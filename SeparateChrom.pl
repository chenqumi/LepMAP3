#chenqumi@20171110
use warnings;
use strict;
use File::Basename;
use FindBin qw($Bin);
use Cwd qw(abs_path getcwd);
BEGIN {
    push (@INC,"$Bin");
}
use Qsub;

my ($data,$lod1,$lod2,$gap) = @ARGV;
die "perl $0 <data.call> <lod1> <lod2> <gap size>" if (@ARGV==0);

my $JAVA = "/lustre/project/og04/shichunwei/biosoft/jre1.8.0_91/bin/java";
my $LP = "/p299/user/og03/chenquan1609/Bin/LepMap3/bin";

$data = abs_path($data);
my $cwd = getcwd();
#qsub parameters
#==============================================
#
my $memory = "40G";
my $thread = 4;
my $queue = "dna.q,rna.q,reseq.q,all.q,super.q";
my $project = "og";
my $max_job = 40;


open SC,">separatechrom.sh" or die $!;
for (my $lod = $lod1; $lod <= $lod2; $lod++) {
    mkdir("LOD$lod");
    my $cmd = "$JAVA -Xmx20G -cp $LP SeparateChromosomes2 data=$data ";
    $cmd .= "lodLimit=$lod lod3Mode=3 sizeLimit=40 > map${lod}.txt 2> sc${lod}.log";
    print SC "sc$lod\.sh\t$cmd\n";
}
close SC;

qsub("separatechrom.sh", "./", "25G", $thread,
     $queue, $project, "SC", $max_job);


#open OM,">ordermarker.sh" or die $!;

#for (my $lod = $lod1; $lod <= $lod2; $lod++) {    
#    foreach my $x (2,3) {
#        my $cmd = "cd LOD$lod && ";
#        $cmd .= "$JAVA -Xmx30G -cp $LP OrderMarkers2 data=$data map=$cwd/map$lod.txt ";
#        $cmd .= "chromosome=$x sexAveraged=1 useKosambi=1 > order$x.txt 2> order$x.log";
#        print OM "order\_$lod\_$x\.sh\t$cmd\n";
#    }
#}

#close OM;

#qsub("ordermarker.sh", "./", $memory, $thread,
#     $queue, $project, "OM", $max_job);