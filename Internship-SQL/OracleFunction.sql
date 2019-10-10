--string: this is a "long" string with "quotes"
--string aint it "beautiful" with all the "quotes" i have, "right?"



select ceil(325.0000000000000001) from dual;
select upper('hiWİSDasdsadRKOW') from dual;


select instr('this is a "long" string with "quotes"', '"', 1,1) from dual;
select instr('this is a "long" string with "quotes"', '"', 1,2) from dual;
select instr('this is a "long" string with "quotes"', '"', 1,3) from dual;
select instr('this is a "long" string with "quotes"', '"', 1,4) from dual;
select substr('this is a "long" string with "quotes"', 1, 4) from dual;

select replace('000000001999', '0') from dual;
select ltrim('+-*call me weyw', '+-*') from dual;





select substr('aint it "beautiful" with all the "quotes" i have"', instr('aint it "beautiful" with all the "quotes" i have', '"', 1,1)+1,
instr('aint it "beautiful" with all the "quotes" i have', '"', 1,2)-1 - instr('aint it "beautiful" with all the "quotes" i have', '"', 1,1))  || 
' ' ||
substr('aint it "beautiful" with all the "quotes" i have', instr('aint it "beautiful" with all the "quotes" i have', '"', 1,3)+1,
instr('aint it "beautiful" with all the "quotes" i have', '"', 1,4)-1 - instr('aint it "beautiful" with all the "quotes" i have', '"', 1,3)) from dual;





select substr('aint it "beautiful" with all the "quotes" i have, "right?"', instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,1)+1,
instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,2)-1 - instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,1))  || ' ' ||

substr('aint it "beautiful" with all the "quotes" i have, "right?"', instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,3)+1,
instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,4)-1 - instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,3)) || ' ' ||

substr('aint it "beautiful" with all the "quotes" i have, "right?"', instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,5)+1,
instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,6)-1 - instr('aint it "beautiful" with all the "quotes" i have, "right?"', '"', 1,5)) from dual;




select replace('aint it "beautiful" with all the "quotes" i have, "right?"', '"', '') from dual;




     
     