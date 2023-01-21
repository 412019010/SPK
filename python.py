from minizinc import Instance, Model, Solver

gecode = Solver.lookup("gecode")

trivial = Model()
trivial.add_string(
    """
    % Kelompok Super

    enum nama = 
    {
    UI,
    BINUS,
    UKRIDA,
    UGM,
    MIT,
    Standford,
    Harvard,
    Caltech,
    Oslo,
    Bergen,
    NTNU,
    UiT,
    Hafizhan,
    Gandhi,
    Aldio,
    Benny,
    Vicky,
    Jufianto,
    Aan,
    Abdur,
    Abdurrahman,
    Sukma,
    Ade,
    Bakti,
    Daniel,
    Dayu,
    Dean,
    Edi,
    Fadil,
    Fahmi,
    Fairuzi,
    Gustian,
    Habil,
    Hermawan,
    Ibnuyohanzah,
    Lia,
    Maksum,
    Risfandanu,
    Adnil,
    Nadia,
    Nanda,
    Nurgivo
    };

    enum detail = 
    {
    kampus,
    mahasiswa
    };

    enum negara = 
    {
    Indonesia,
    USA,
    Norwegia
    };

    enum jurusan = 
    {
    informatika,
    manajemen,
    kedokteran,
    sastra,
    hukum,
    elektro,
    pertanian,
    kimia
    };

    int: IPK = 1;
    int: Detail = 2;
    int: Negara = 3;
    int: MinIPK = 4;
    int: Jurusan = 5;

    % Data lengkap
    array[nama,1..5] of int: data =
    array2d(nama, 1..5,
    [
    0,kampus,Indonesia,390,sastra,
    0,kampus,Indonesia,350,informatika,
    0,kampus,Indonesia,300,kedokteran,
    0,kampus,Indonesia,350,manajemen,
    0,kampus,USA,400,sastra,
    0,kampus,USA,390,informatika,
    0,kampus,USA,380,hukum,
    0,kampus,USA,380,elektro,
    0,kampus,Norwegia,350,hukum,
    0,kampus,Norwegia,350,elektro,
    0,kampus,Norwegia,370,pertanian,
    0,kampus,Norwegia,375,kimia,
    392,mahasiswa,USA,0,sastra,
    398,mahasiswa,USA,0,sastra,
    400,mahasiswa,Norwegia,0,sastra,
    357,mahasiswa,USA,0,informatika,
    354,mahasiswa,USA,0,kedokteran,
    356,mahasiswa,USA,0,kedokteran,
    355,mahasiswa,Norwegia,0,kedokteran,
    353,mahasiswa,Norwegia,0,kedokteran,
    400,mahasiswa,USA,0,kedokteran,
    396,mahasiswa,Norwegia,0,manajemen,
    353,mahasiswa,USA,0,manajemen,
    353,mahasiswa,USA,0,manajemen,
    400,mahasiswa,Indonesia,0,sastra,
    391,mahasiswa,Indonesia,0,informatika,
    399,mahasiswa,Indonesia,0,informatika,
    400,mahasiswa,Indonesia,0,informatika,
    381,mahasiswa,Norwegia,0,hukum,
    390,mahasiswa,Norwegia,0,elektro,
    352,mahasiswa,USA,0,hukum,
    379,mahasiswa,USA,0,hukum,
    351,mahasiswa,USA,0,hukum,
    382,mahasiswa,USA,0,hukum,
    358,mahasiswa,USA,0,hukum,
    353,mahasiswa,USA,0,elektro,
    351,mahasiswa,USA,0,elektro,
    391,mahasiswa,USA,0,elektro,
    395,mahasiswa,USA,0,elektro,
    399,mahasiswa,USA,0,elektro,
    378,mahasiswa,Indonesia,0,pertanian,
    380,mahasiswa,Indonesia,0,kimia,
    ]);

    % Mahasiswa daftar ke kampus, kampus didaftar oleh mahasiswa
    array[nama] of set of detail: daftar =
    [
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {mahasiswa},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    {kampus},
    ];

    array[nama] of var nama: x;
    array[nama] of var 0..1: sesuai;

    constraint
      forall(p in nama) (
        x[p] != p
      )
      /\ 
      forall(p in nama) (
        % Kampus hanya bisa dipilih mahasiswa dan mahasiswa memilih kampus
        data[x[p],Detail] in daftar[p] /\ 

        % IPK mahasiswa harus memenuhi standart IPK kampus
        data[x[p],IPK] >= data[p,MinIPK]/\ 

        % Negara ga boleh sama
        data[x[p],Negara] != data[p,Negara] /\ 
        
        % Jurusan yang dicari harus sama dengan jurusan mahasiswa
        data[x[p],Jurusan] = data[p,Jurusan] /\ 

        sesuai[p] = if p = x[x[p]] then 1 else 0 endif
      )
    ;

    solve satisfy;

    output 
    [
      if fix(sesuai[p]) = 1 /\ p < fix(x[p]) then 
        "\(p) = \(x[p])\\n"
      else 
        ""
      endif
      | p in nama
    ];
    """
)
instance = Instance(gecode, trivial)

result = instance.solve(intermediate_solutions=True)
for i in range(len(result)):
    print(result[i])
