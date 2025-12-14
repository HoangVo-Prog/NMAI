% Tham số bài toán
dung_tich_binh_1(4).     % Vx
dung_tich_binh_2(3).     % Vy
muc_tieu(2).             % z

% Trạng thái bắt đầu
trang_thai_bat_dau(trang_thai(0, 0)).

% Hành động: đổ đầy bình 1
pha_nuoc(trang_thai(X, Y), trang_thai(Vx, Y), 'Do day binh 1') :-
    dung_tich_binh_1(Vx),
    X < Vx.

% Hành động: đổ đầy bình 2
pha_nuoc(trang_thai(X, Y), trang_thai(X, Vy), 'Do day binh 2') :-
    dung_tich_binh_2(Vy),
    Y < Vy.

% Hành động: đổ hết bình 1
pha_nuoc(trang_thai(X, Y), trang_thai(0, Y), 'Do het binh 1') :-
    X > 0.

% Hành động: đổ hết bình 2
pha_nuoc(trang_thai(X, Y), trang_thai(X, 0), 'Do het binh 2') :-
    Y > 0.

% Hành động: đổ từ bình 1 sang bình 2
pha_nuoc(trang_thai(X, Y), trang_thai(NewX, NewY), 'Do tu Binh 1 sang Binh 2') :-
    X > 0,
    dung_tich_binh_2(Vy),
    Y < Vy,
    ChoTrong is Vy - Y,
    min_2(X, ChoTrong, LuongDo),
    NewX is X - LuongDo,
    NewY is Y + LuongDo.

% Hành động: đổ từ bình 2 sang bình 1
pha_nuoc(trang_thai(X, Y), trang_thai(NewX, NewY), 'Do tu Binh 2 sang Binh 1') :-
    Y > 0,
    dung_tich_binh_1(Vx),
    X < Vx,
    ChoTrong is Vx - X,
    min_2(Y, ChoTrong, LuongDo),
    NewX is X + LuongDo,
    NewY is Y - LuongDo.

% min_2(A, B, M) :- M là giá trị nhỏ hơn giữa A và B
min_2(A, B, A) :- A =< B.
min_2(A, B, B) :- A >  B.

% Điều kiện dừng: đạt mục tiêu ở một trong hai bình
dat_muc_tieu(trang_thai(X, Y)) :-
    muc_tieu(Z),
    (X =:= Z ; Y =:= Z).

% Tìm đường đi (DFS, tránh lặp)
tim_duong(TrangThai, _, []) :-
    dat_muc_tieu(TrangThai).

tim_duong(TrangThaiHienTai, DaDi, [HanhDong | CacBuoc]) :-
    pha_nuoc(TrangThaiHienTai, TrangThaiMoi, HanhDong),
    \+ member(TrangThaiMoi, DaDi),
    tim_duong(TrangThaiMoi, [TrangThaiHienTai | DaDi], CacBuoc).

% In kết quả
in_ket_qua([]).
in_ket_qua([H | T]) :-
    write(H), nl,
    in_ket_qua(T).

% Hàm chạy chính
giai_quyet :-
    trang_thai_bat_dau(Start),
    tim_duong(Start, [Start], CachLam),
    in_ket_qua(CachLam).
