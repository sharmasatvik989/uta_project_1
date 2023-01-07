; sum an array
        go   0
0       ld   1	.Num
	ldi  2	.a1	
        ldi  3	.a1
        add  3	1 
        ldi  4	.a1
        add  4	1
        add  4	1
.loop	ld   5  *2
        add  5  *3
        st   5  *4
        inc  2 
        inc  3
        inc  4 
        dec  1
        bnz  1  .loop
        sys  1  16
        dw   0 
.Num    dw   4
.a1 	dw   1
        dw   2
        dw   3
        dw   4
        dw   5
        dw   6
        dw   7
        dw   8
        dw   0
	dw   0
	dw   0
	dw   0
0       ld   1	.Num
	ldi  2	.a1	
        ldi  3	.a1
        add  3	1 
        ldi  4	.a1
        add  4	1
        add  4	1
.loop	ld   5  *2
        add  5  *3
        st   5  *4
        inc  2 
        inc  3
        inc  4 
        dec  1
        bnz  1  .loop
        sys  1  16
        dw   0 
.Num    dw   4
.a1 	dw   1
        dw   5
        dw   6
        dw   7
        dw   8
        dw   5
        dw   3
        dw   3
        dw   0
	dw   0
	dw   0
	dw   0
        end


