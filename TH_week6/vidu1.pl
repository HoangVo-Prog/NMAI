% Quan hệ cha mẹ
parent(marry, bill).
parent(tom, bill).
parent(tom, liz).
parent(bill, ann).
parent(bill, sue).
parent(sue, jim).

% Giới tính
man(tom).
man(bill).
man(jim).

woman(liz).
woman(sue).
woman(ann).
woman(marry).

% Y là con của X nếu X là cha/mẹ của Y
child(Y,X) :- parent(X,Y).

% X là mẹ của Y nếu X là cha/mẹ và là nữ
mother(X,Y) :- parent(X,Y), woman(X).

% X là ông/bà của Z nếu X là cha/mẹ của Y và Y là cha/mẹ của Z
grandparent(X,Z) :- parent(X,Y), parent(Y,Z).

% Hai người khác nhau
different(X,Y) :- X \== Y.

% X là chị/em gái của Y nếu cùng cha/mẹ, X là nữ và X khác Y
sister(X,Y) :- parent(Z,X), parent(Z,Y), woman(X), different(X,Y).
