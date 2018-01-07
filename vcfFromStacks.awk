#awk [-verror=0.001] -f vcfFromStacks.awk input.vcf >output.vcf
BEGIN{
	FS="\t"
	OFS="\t"
	if (error == "")
		error = 0.001

	logError = log(error)
	log1MError = log(1 - error)
	logHalf = log(0.5)

	const1log10 = 1.0 / log(10)
}

function phred(p1, p2, p3     ,max,ret){
	max = p1;
	if (p2 > max)
		max = p2
	if (p3 > max)
		max = p3

	p1 -= max
	p2 -= max
	p3 -= max

	if (p1 <= -58.7)
		ret = "255"
	else
		ret = -int(10 * p1 * const1log10 + 0.5)

	if (p2 <= -58.7)
		ret = ret ",255"
	else
		ret = ret "," (-int(10 * p2 * const1log10 + 0.5))

	if (p3 <= -58.7)
		ret = ret ",255"
	else
		ret = ret "," (-int(10 * p3 * const1log10 + 0.5))
	return ret
}

{
	if ($1 ~ /^#/)
		print
	else {
		n = split($9, format, ":")
		

		for (j = 1; j <= n; ++j)
			if (format[j] == "AD")
				break
		numAlleles = split($4 "," $5, alleles, ",")

		if (j <= n && numAlleles == 2) {
			$9 = $9 ":PL"
			for (i = 10; i <= NF; ++i) {
				split($i, format, ":")
				split(format[j], ad, ",")

				p1 = logError * ad[2] + log1MError * ad[1] #(1 - error) ** ad[1] * error ** ad[2]
				p2 = logHalf * (ad[1] + ad[2])             #0.5 ** (ad[1] + ad[2])
				p3 = logError * ad[1] + log1MError * ad[2] #error ** ad[1] * (1 - error) ** ad[2]
				$i = $i ":" phred(p1, p2, p3)
			}
			print
		}
	
	}
}
