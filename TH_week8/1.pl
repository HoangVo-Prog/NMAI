% gcd(X, Y, D) :- D là ước chung lớn nhất của X và Y.

% Trường hợp neo: hai số bằng nhau
gcd(X, X, X).

% Nếu X < Y thì giảm Y và gọi lại
gcd(X, Y, D) :-
    X < Y,
    Y1 is Y - X,
    gcd(X, Y1, D).

% Nếu X > Y thì giảm X và gọi lại
gcd(X, Y, D) :-
    X > Y,
    X1 is X - Y,
    gcd(X1, Y, D).
