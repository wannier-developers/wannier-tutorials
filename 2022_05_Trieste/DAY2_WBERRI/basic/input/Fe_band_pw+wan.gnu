set style data dots
set key below
set term pdf
set output "Fe_bands.pdf"
set xrange [0: 6.72791]
set yrange [  3.44754 : 46.48114]
set arrow from  2.18927,   3.44754 to  2.18927,  46.48114 nohead
set arrow from  4.08523,   3.44754 to  4.08523,  46.48114 nohead
set arrow from  5.17987,   3.44754 to  5.17987,  46.48114 nohead
set xtics ("G"  0.00000,"H"  2.18927,"P"  4.08523,"N"  5.17987,"G"  6.72791 )
 plot "Fe_band.dat" u 1:2 w l lw 2  title "wannier90", "Fe_bands_pw.dat" u ($1*2*pi/(5.4235*0.529)):2 w p ps 0.5 pt 6 title "bands.x", 12.61 w l lw 3 lc black title "EF", 30 w l lw 3 title "dis_froz_max"
