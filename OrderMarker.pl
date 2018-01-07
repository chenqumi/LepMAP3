#chenqumi@20171123
use warnings;
use strict;
use File::Basename;
use FindBin qw($Bin);
use Cwd qw(abs_path getcwd);
BEGIN {
    push (@INC,"$Bin");
}
use Qsub;

my ($data,$map,$lg,$iter) = @ARGV;
die "perl $0 <datafile> <mapfile> <number of LG> <iterate times>" if (@ARGV==0);

my $JAVA = "/lustre/project/og04/shichunwei/biosoft/jre1.8.0_91/bin/java";
my $LM = "/p299/user/og03/chenquan1609/Bin/LepMap3/bin";

$data = abs_path($data);
$map = abs_path($map);
my $cwd = getcwd();
#qsub parameters
#==============================================
#
my $memory = "40G";
my $thread = 4;
my $queue = "dna.q,rna.q,reseq.q,all.q,super.q";
my $project = "og";
my $max_job = 40;

my $shell = "$cwd/Shell";
mkdir($shell);

open OR,">ordermarker.sh" or die $!;

for (my $i = 1; $i <= $iter; $i++) {
    my $dir = "repeat${i}";
    $dir = abs_path($dir);
    mkdir ($dir);
    for (my $num = 1; $num <= $lg; $num++) {
        my $cmd = "cd $dir && ";
        $cmd .= "$JAVA -Xmx30G -cp $LM OrderMarkers2 ";
        $cmd .= "data=$data map=$map sexAveraged=1 ";
        $cmd .= "chromosome=${num} useKosambi=1 ";
        $cmd .= "> order${num}\.txt 2> order${num}\.log";
        print OR "order\_${i}\_${num}\.sh\t$cmd\n";
    }
}

close OR;

qsub("ordermarker.sh", $shell, $memory, $thread,
     $queue, $project, "OM", $max_job);