from abc import ABC, abstractmethod
from datetime import datetime
import re

# ===============================
# LEVEL 1: BASIC CLASS (MUDAH)
# ===============================

class Mahasiswa:
    """
    Level 1: Basic Class - Konsep dasar OOP
    Fitur: constructor, instance method, basic attributes
    """
    
    def __init__(self, nama, nim, jurusan):
        self.nama = nama
        self.nim = nim
        self.jurusan = jurusan
        print(f"✓ Mahasiswa {nama} berhasil terdaftar")
    
    def perkenalan(self):
        return f"Nama: {self.nama}, NIM: {self.nim}, Jurusan: {self.jurusan}"
    
    def ubah_jurusan(self, jurusan_baru):
        old_jurusan = self.jurusan
        self.jurusan = jurusan_baru
        print(f"Jurusan {self.nama} diubah dari {old_jurusan} ke {jurusan_baru}")


# ===============================
# LEVEL 2: CONSTRUCTOR & METHOD (SEDANG)
# ===============================

class SistemPembayaran:
    """
    Level 2: Constructor & Method - Method kompleks dengan validasi
    Fitur: default parameters, input validation, return values, error handling
    """
    
    def __init__(self, nama_mahasiswa, nim, saldo_awal=0):
        self.nama_mahasiswa = nama_mahasiswa
        self.nim = nim
        self.saldo = saldo_awal
        self.riwayat_transaksi = []
        print(f"✓ Akun pembayaran {nama_mahasiswa} dibuat dengan saldo Rp {saldo_awal:,}")
    
    def top_up(self, jumlah):
        if jumlah <= 0:
            print("❌ Error: Jumlah top up harus lebih dari 0")
            return False
        
        self.saldo += jumlah
        self.riwayat_transaksi.append(f"Top Up: +Rp {jumlah:,}")
        print(f"✓ Top up Rp {jumlah:,} berhasil. Saldo: Rp {self.saldo:,}")
        return True
    
    def bayar_spp(self, jumlah):
        if jumlah <= 0:
            print("❌ Error: Jumlah pembayaran harus lebih dari 0")
            return False
        
        if jumlah > self.saldo:
            print(f"❌ Error: Saldo tidak mencukupi. Saldo: Rp {self.saldo:,}")
            return False
        
        self.saldo -= jumlah
        self.riwayat_transaksi.append(f"SPP: -Rp {jumlah:,}")
        print(f"✓ Pembayaran SPP Rp {jumlah:,} berhasil. Sisa saldo: Rp {self.saldo:,}")
        return True
    
    def transfer_ke_teman(self, akun_tujuan, jumlah):
        if not isinstance(akun_tujuan, SistemPembayaran):
            print("❌ Error: Akun tujuan tidak valid")
            return False
        
        if jumlah > self.saldo:
            print(f"❌ Error: Saldo tidak mencukupi untuk transfer")
            return False
        
        self.saldo -= jumlah
        akun_tujuan.saldo += jumlah
        
        self.riwayat_transaksi.append(f"Transfer ke {akun_tujuan.nama_mahasiswa}: -Rp {jumlah:,}")
        akun_tujuan.riwayat_transaksi.append(f"Transfer dari {self.nama_mahasiswa}: +Rp {jumlah:,}")
        
        print(f"✓ Transfer Rp {jumlah:,} ke {akun_tujuan.nama_mahasiswa} berhasil")
        return True
    
    def get_saldo(self):
        return self.saldo


# ===============================
# LEVEL 3: INHERITANCE (SEDANG-SULIT)
# ===============================

class PersonAkademik:
    """
    Level 3: Inheritance - Parent class
    Fitur: base class, method inheritance, constructor chaining
    """
    
    def __init__(self, nama, id_person, email):
        self.nama = nama
        self.id_person = id_person
        self.email = email
        self.status_aktif = True
        print(f"✓ Person akademik {nama} terdaftar")
    
    def info_dasar(self):
        return f"Nama: {self.nama}, ID: {self.id_person}, Email: {self.email}"
    
    def update_email(self, email_baru):
        self.email = email_baru
        print(f"Email {self.nama} diperbarui ke {email_baru}")


class MahasiswaTingkatLanjut(PersonAkademik):
    """
    Child class dari PersonAkademik dengan fitur tambahan
    """
    
    def __init__(self, nama, nim, email, jurusan, angkatan):
        super().__init__(nama, nim, email)  # Constructor chaining
        self.jurusan = jurusan
        self.angkatan = angkatan
        self.mata_kuliah = []
        self.ipk = 0.0
        print(f"✓ Mahasiswa {nama} angkatan {angkatan} terdaftar di {jurusan}")
    
    def ambil_mata_kuliah(self, nama_mk, sks):
        self.mata_kuliah.append({"nama": nama_mk, "sks": sks, "nilai": None})
        print(f"✓ {self.nama} mengambil mata kuliah {nama_mk} ({sks} SKS)")
    
    def input_nilai(self, nama_mk, nilai):
        for mk in self.mata_kuliah:
            if mk["nama"] == nama_mk:
                mk["nilai"] = nilai
                print(f"✓ Nilai {nama_mk} untuk {self.nama}: {nilai}")
                self._hitung_ipk()
                return True
        print(f"❌ Mata kuliah {nama_mk} tidak ditemukan")
        return False
    
    def _hitung_ipk(self):
        """Private method untuk menghitung IPK"""
        if not self.mata_kuliah:
            return
        
        total_sks = sum(mk["sks"] for mk in self.mata_kuliah if mk["nilai"] is not None)
        if total_sks == 0:
            return
        
        total_nilai = sum(mk["nilai"] * mk["sks"] for mk in self.mata_kuliah if mk["nilai"] is not None)
        self.ipk = total_nilai / total_sks
    
    def info_dasar(self):
        """Override method parent dengan informasi tambahan"""
        base_info = super().info_dasar()
        return f"{base_info}, Jurusan: {self.jurusan}, IPK: {self.ipk:.2f}"


class Dosen(PersonAkademik):
    """
    Child class lain dari PersonAkademik
    """
    
    def __init__(self, nama, nip, email, fakultas):
        super().__init__(nama, nip, email)
        self.fakultas = fakultas
        self.mata_kuliah_diampu = []
        print(f"✓ Dosen {nama} terdaftar di fakultas {fakultas}")
    
    def ampu_mata_kuliah(self, nama_mk):
        self.mata_kuliah_diampu.append(nama_mk)
        print(f"✓ Prof. {self.nama} mengampu mata kuliah {nama_mk}")
    
    def info_dasar(self):
        """Override method parent"""
        base_info = super().info_dasar()
        return f"{base_info}, Fakultas: {self.fakultas}"


# ===============================
# LEVEL 4: ENCAPSULATION & PROPERTY (SULIT)
# ===============================

class MahasiswaIPK:
    """
    Level 4: Encapsulation & Property - Private attributes, getter/setter, validation
    Fitur: private attributes, property decorator, data validation, computed properties
    """
    
    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim
        self._ipk = 0.0  # Private attribute
        self._total_sks = 0
        self._total_nilai_kali_sks = 0.0
        self._semester_aktif = 1
        print(f"✓ Mahasiswa IPK {nama} initialized")
    
    @property
    def ipk(self):
        """Getter untuk IPK - tidak bisa diubah langsung"""
        return self._ipk
    
    @property
    def semester(self):
        """Getter untuk semester"""
        return self._semester_aktif
    
    @semester.setter
    def semester(self, nilai):
        """Setter untuk semester dengan validasi"""
        if not isinstance(nilai, int):
            raise TypeError("Semester harus berupa integer")
        if nilai < 1 or nilai > 14:
            raise ValueError("Semester harus antara 1-14")
        
        old_semester = self._semester_aktif
        self._semester_aktif = nilai
        print(f"✓ Semester {self.nama} diperbarui dari {old_semester} ke {nilai}")
    
    @property
    def status_akademik(self):
        """Computed property berdasarkan IPK"""
        if self._ipk >= 3.5:
            return "Cumlaude"
        elif self._ipk >= 3.0:
            return "Sangat Baik"
        elif self._ipk >= 2.5:
            return "Baik"
        elif self._ipk >= 2.0:
            return "Cukup"
        else:
            return "Kurang"
    
    @property
    def bisa_lulus(self):
        """Computed property untuk syarat kelulusan"""
        return self._ipk >= 2.0 and self._total_sks >= 144
    
    def tambah_nilai(self, mata_kuliah, sks, nilai):
        """Method untuk menambah nilai dan otomatis recalculate IPK"""
        if not (0 <= nilai <= 4.0):
            print("❌ Error: Nilai harus antara 0.0 - 4.0")
            return False
        
        if sks <= 0:
            print("❌ Error: SKS harus lebih dari 0")
            return False
        
        self._total_sks += sks
        self._total_nilai_kali_sks += (nilai * sks)
        
        # Recalculate IPK
        if self._total_sks > 0:
            self._ipk = self._total_nilai_kali_sks / self._total_sks
        
        print(f"✓ Nilai {mata_kuliah}: {nilai} ({sks} SKS) ditambahkan")
        print(f"  IPK terbaru: {self._ipk:.2f}, Status: {self.status_akademik}")
        return True
    
    def info_lengkap(self):
        return (f"Nama: {self.nama}, NIM: {self.nim}, "
                f"Semester: {self._semester_aktif}, IPK: {self._ipk:.2f}, "
                f"Total SKS: {self._total_sks}, Status: {self.status_akademik}, "
                f"Bisa Lulus: {'Ya' if self.bisa_lulus else 'Belum'}")


# ===============================
# LEVEL 5: STATIC & CLASS METHOD (SULIT)
# ===============================

class UtilitasAkademik:
    """
    Level 5: Static & Class Method - Method yang tidak terikat instance
    Fitur: static method, class method, utility functions, parsing
    """
    
    # Class variable
    _skala_nilai = {
        'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'E': 0.0
    }
    
    @staticmethod
    def hitung_ipk(daftar_nilai_sks):
        """
        Static method untuk menghitung IPK
        Args: list of tuples [(nilai, sks), ...]
        """
        if not daftar_nilai_sks:
            return 0.0
        
        total_sks = sum(sks for _, sks in daftar_nilai_sks)
        if total_sks == 0:
            return 0.0
        
        total_nilai_kali_sks = sum(nilai * sks for nilai, sks in daftar_nilai_sks)
        return total_nilai_kali_sks / total_sks
    
    @staticmethod
    def konversi_huruf_ke_angka(nilai_huruf):
        """Static method untuk konversi nilai huruf ke angka"""
        return UtilitasAkademik._skala_nilai.get(nilai_huruf.upper(), 0.0)
    
    @staticmethod
    def prediksi_kelulusan_tepat_waktu(ipk_sekarang, semester_sekarang):
        """Static method untuk prediksi kelulusan"""
        if semester_sekarang <= 0 or semester_sekarang > 8:
            return "Data tidak valid"
        
        if ipk_sekarang >= 3.0:
            return "Sangat Berpeluang Lulus Tepat Waktu"
        elif ipk_sekarang >= 2.5:
            return "Berpeluang Lulus Tepat Waktu dengan Usaha Ekstra"
        elif ipk_sekarang >= 2.0:
            return "Perlu Perbaikan Signifikan"
        else:
            return "Risiko Tinggi Tidak Lulus Tepat Waktu"
    
    @classmethod
    def dari_string_transkrip(cls, data_string):
        """
        Class method untuk parsing string transkrip
        Format: "MK1:A:3,MK2:B:2,MK3:A-:4"
        """
        try:
            mata_kuliah_list = []
            items = data_string.split(',')
            
            for item in items:
                parts = item.strip().split(':')
                if len(parts) != 3:
                    continue
                
                nama_mk = parts[0].strip()
                nilai_huruf = parts[1].strip()
                sks = int(parts[2].strip())
                nilai_angka = cls.konversi_huruf_ke_angka(nilai_huruf)
                
                mata_kuliah_list.append({
                    'nama': nama_mk,
                    'nilai_huruf': nilai_huruf,
                    'nilai_angka': nilai_angka,
                    'sks': sks
                })
            
            return mata_kuliah_list
            
        except Exception as e:
            print(f"❌ Error parsing transkrip: {e}")
            return []
    
    @classmethod
    def analisis_transkrip(cls, data_string):
        """Class method untuk analisis lengkap transkrip"""
        mata_kuliah_list = cls.dari_string_transkrip(data_string)
        if not mata_kuliah_list:
            return None
        
        # Hitung statistik
        daftar_nilai_sks = [(mk['nilai_angka'], mk['sks']) for mk in mata_kuliah_list]
        ipk = cls.hitung_ipk(daftar_nilai_sks)
        total_sks = sum(mk['sks'] for mk in mata_kuliah_list)
        
        return {
            'mata_kuliah': mata_kuliah_list,
            'ipk': ipk,
            'total_sks': total_sks,
            'jumlah_mk': len(mata_kuliah_list),
            'rata_rata_sks': total_sks / len(mata_kuliah_list) if mata_kuliah_list else 0
        }


# ===============================
# LEVEL 6: ABSTRACT CLASS & MULTIPLE INHERITANCE (SANGAT SULIT)
# ===============================

class Aktivitas(ABC):
    """Abstract base class untuk semua aktivitas akademik"""
    
    def __init__(self, nama_aktivitas):
        self.nama_aktivitas = nama_aktivitas
        self.tanggal_mulai = None
        self.status = "Belum Dimulai"
    
    @abstractmethod
    def mulai_aktivitas(self):
        """Abstract method yang harus diimplementasi child class"""
        pass
    
    @abstractmethod
    def selesai_aktivitas(self):
        """Abstract method untuk menyelesaikan aktivitas"""
        pass
    
    def set_tanggal_mulai(self, tanggal):
        self.tanggal_mulai = tanggal


class Penelitian:
    """Mixin class untuk kemampuan penelitian"""
    
    def __init__(self):
        self.topik_penelitian = None
        self.status_penelitian = "Belum Dimulai"
        self.publikasi = []
    
    def set_topik_penelitian(self, topik):
        self.topik_penelitian = topik
        self.status_penelitian = "Sedang Berlangsung"
        print(f"✓ Topik penelitian ditetapkan: {topik}")
    
    def tambah_publikasi(self, judul_paper, jurnal):
        self.publikasi.append({"judul": judul_paper, "jurnal": jurnal})
        print(f"✓ Publikasi ditambahkan: {judul_paper} di {jurnal}")
    
    def get_info_penelitian(self):
        return {
            "topik": self.topik_penelitian,
            "status": self.status_penelitian,
            "jumlah_publikasi": len(self.publikasi)
        }


class Organisasi:
    """Mixin class untuk kemampuan organisasi"""
    
    def __init__(self):
        self.jabatan_organisasi = []
        self.pengalaman_kepemimpinan = []
    
    def tambah_jabatan(self, nama_organisasi, jabatan, periode):
        self.jabatan_organisasi.append({
            "organisasi": nama_organisasi,
            "jabatan": jabatan,
            "periode": periode
        })
        print(f"✓ Jabatan ditambahkan: {jabatan} di {nama_organisasi} ({periode})")
    
    def tambah_pengalaman_kepemimpinan(self, kegiatan, peran):
        self.pengalaman_kepemimpinan.append({"kegiatan": kegiatan, "peran": peran})
        print(f"✓ Pengalaman kepemimpinan: {peran} dalam {kegiatan}")
    
    def get_info_organisasi(self):
        return {
            "total_jabatan": len(self.jabatan_organisasi),
            "total_pengalaman": len(self.pengalaman_kepemimpinan)
        }


class MahasiswaAktif(Aktivitas, Penelitian, Organisasi):
    """
    Level 6: Multiple Inheritance & Abstract Class
    Class yang inherit dari abstract class dan multiple mixin classes
    """
    
    def __init__(self, nama, nim, jurusan):
        Aktivitas.__init__(self, f"Studi {nama}")
        Penelitian.__init__(self)
        Organisasi.__init__(self)
        
        self.nama = nama
        self.nim = nim
        self.jurusan = jurusan
        self.semester_aktif = 1
        print(f"✓ Mahasiswa Aktif {nama} created dengan multiple inheritance")
    
    def mulai_aktivitas(self):
        """Implementasi abstract method dari Aktivitas"""
        self.status = "Sedang Studi"
        self.set_tanggal_mulai(datetime.now().strftime("%Y-%m-%d"))
        print(f"✓ {self.nama} memulai aktivitas akademik pada {self.tanggal_mulai}")
    
    def selesai_aktivitas(self):
        """Implementasi abstract method dari Aktivitas"""
        self.status = "Lulus"
        print(f"✓ {self.nama} menyelesaikan studi dengan status: {self.status}")
    
    def naik_semester(self):
        self.semester_aktif += 1
        print(f"✓ {self.nama} naik ke semester {self.semester_aktif}")
    
    def profil_lengkap(self):
        """Method untuk menampilkan profil lengkap dengan info dari semua parent class"""
        info_penelitian = self.get_info_penelitian()
        info_organisasi = self.get_info_organisasi()
        
        return {
            "identitas": {
                "nama": self.nama,
                "nim": self.nim,
                "jurusan": self.jurusan,
                "semester": self.semester_aktif
            },
            "aktivitas": {
                "nama_aktivitas": self.nama_aktivitas,
                "status": self.status,
                "tanggal_mulai": self.tanggal_mulai
            },
            "penelitian": info_penelitian,
            "organisasi": info_organisasi
        }


# ===============================
# BONUS: SINGLETON PATTERN
# ===============================

class SistemAkademikDatabase:
    """
    Bonus: Singleton Pattern - Hanya satu instance database
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.mahasiswa_data = {}
            self.connected = False
            self.query_count = 0
            self._initialized = True
            print("✓ Database Sistem Akademik initialized (Singleton)")
    
    def connect(self):
        self.connected = True
        print("✓ Database connected")
    
    def disconnect(self):
        self.connected = False
        print("✓ Database disconnected")
    
    def tambah_mahasiswa(self, nim, data_mahasiswa):
        if not self.connected:
            print("❌ Database not connected")
            return False
        
        self.mahasiswa_data[nim] = data_mahasiswa
        self.query_count += 1
        print(f"✓ Mahasiswa {nim} ditambahkan ke database")
        return True
    
    def get_mahasiswa(self, nim):
        if not self.connected:
            print("❌ Database not connected")
            return None
        
        self.query_count += 1
        return self.mahasiswa_data.get(nim)
    
    def get_stats(self):
        return {
            "total_mahasiswa": len(self.mahasiswa_data),
            "total_queries": self.query_count,
            "connected": self.connected
        }


# ===============================
# DEMO LENGKAP SEMUA LEVEL
# ===============================

def demo_sistem_mahasiswa():
    print("=" * 80)
    print("🎓 DEMO SISTEM MAHASISWA - 6 LEVEL KESULITAN OOP")
    print("=" * 80)
    
    # LEVEL 1: BASIC CLASS
    print("\n📚 LEVEL 1: BASIC CLASS")
    print("-" * 40)
    mhs_basic = Mahasiswa("Alice Johnson", "2023001", "Teknik Informatika")
    print(mhs_basic.perkenalan())
    mhs_basic.ubah_jurusan("Sistem Informasi")
    
    # LEVEL 2: CONSTRUCTOR & METHOD
    print("\n💰 LEVEL 2: CONSTRUCTOR & METHOD (PEMBAYARAN)")
    print("-" * 40)
    pembayaran_alice = SistemPembayaran("Alice Johnson", "2023001", 500000)
    pembayaran_bob = SistemPembayaran("Bob Smith", "2023002", 300000)
    
    pembayaran_alice.top_up(200000)
    pembayaran_alice.bayar_spp(150000)
    pembayaran_alice.transfer_ke_teman(pembayaran_bob, 100000)
    
    print(f"Saldo Alice: Rp {pembayaran_alice.get_saldo():,}")
    print(f"Saldo Bob: Rp {pembayaran_bob.get_saldo():,}")
    
    # LEVEL 3: INHERITANCE
    print("\n👥 LEVEL 3: INHERITANCE")
    print("-" * 40)
    mhs_lanjut = MahasiswaTingkatLanjut("Charlie Brown", "2023003", "charlie@univ.ac.id", 
                                        "Teknik Informatika", 2023)
    dosen = Dosen("Dr. Smith", "NIP001", "smith@univ.ac.id", "Teknik")
    
    mhs_lanjut.ambil_mata_kuliah("Algoritma", 3)
    mhs_lanjut.ambil_mata_kuliah("Database", 3)
    mhs_lanjut.input_nilai("Algoritma", 3.7)
    mhs_lanjut.input_nilai("Database", 3.3)
    
    dosen.ampu_mata_kuliah("Algoritma")
    
    print("Info Mahasiswa:", mhs_lanjut.info_dasar())
    print("Info Dosen:", dosen.info_dasar())
    
    # LEVEL 4: ENCAPSULATION & PROPERTY
    print("\n🔒 LEVEL 4: ENCAPSULATION & PROPERTY")
    print("-" * 40)
    mhs_ipk = MahasiswaIPK("Diana Prince", "2023004")
    
    mhs_ipk.tambah_nilai("Matematika", 4, 3.7)
    mhs_ipk.tambah_nilai("Fisika", 3, 3.3)
    mhs_ipk.tambah_nilai("Kimia", 3, 3.0)
    
    print(f"IPK (read-only): {mhs_ipk.ipk}")
    print(f"Status Akademik: {mhs_ipk.status_akademik}")
    
    # Test property setter
    mhs_ipk.semester = 3
    print(f"Semester: {mhs_ipk.semester}")
    
    print(mhs_ipk.info_lengkap())
    
    # LEVEL 5: STATIC & CLASS METHOD
    print("\n🔧 LEVEL 5: STATIC & CLASS METHOD")
    print("-" * 40)
    
    # Static method
    nilai_sks_data = [(3.7, 4), (3.3, 3), (3.0, 3)]
    ipk_result = UtilitasAkademik.hitung_ipk(nilai_sks_data)
    print(f"IPK dari static method: {ipk_result:.2f}")
    
    nilai_huruf = UtilitasAkademik.konversi_huruf_ke_angka("A-")
    print(f"Nilai A- = {nilai_huruf}")
    
    prediksi = UtilitasAkademik.prediksi_kelulusan_tepat_waktu(3.5, 4)
    print(f"Prediksi kelulusan: {prediksi}")
    
    # Class method
    transkrip_string = "Algoritma:A:3,Database:B+:3,Matematika:A-:4,Fisika:B:3"
    analisis = UtilitasAkademik.analisis_transkrip(transkrip_string)
    if analisis:
        print(f"Hasil analisis transkrip:")
        print(f"  - IPK: {analisis['ipk']:.2f}")
        print(f"  - Total SKS: {analisis['total_sks']}")
        print(f"  - Jumlah MK: {analisis['jumlah_mk']}")
    
    # LEVEL 6: ABSTRACT CLASS & MULTIPLE INHERITANCE
    print("\n🏆 LEVEL 6: ABSTRACT CLASS & MULTIPLE INHERITANCE")
    print("-" * 40)
    
    mhs_aktif = MahasiswaAktif("Eva Martinez", "2023005", "Teknik Informatika")
    
    # Dari Aktivitas (Abstract class)
    mhs_aktif.mulai_aktivitas()
    
    # Dari Penelitian (Mixin)
    mhs_aktif.set_topik_penelitian("Machine Learning untuk Prediksi Cuaca")
    mhs_aktif.tambah_publikasi("AI Weather Prediction", "IEEE Transactions")
    
    # Dari Organisasi (Mixin)
    mhs_aktif.tambah_jabatan("Himpunan Mahasiswa TI", "Ketua", "2023-2024")
    mhs_aktif.tambah_pengalaman_kepemimpinan("Seminar AI", "Ketua Panitia")
    
    # Method dari class sendiri
    mhs_aktif.naik_semester()
    mhs_aktif.naik_semester()
    
    # Profil lengkap menggabungkan semua inheritance
    profil = mhs_aktif.profil_lengkap()
    print("Profil Lengkap Multiple Inheritance:")
    for kategori, data in profil.items():
        print(f"  {kategori.title()}: {data}")
    
    # BONUS: SINGLETON PATTERN
    print("\n🔄 BONUS: SINGLETON PATTERN")
    print("-" * 40)
    
    # Test singleton - dua instance harus sama
    db1 = SistemAkademikDatabase()
    db2 = SistemAkademikDatabase()
    
    print(f"db1 adalah db2: {db1 is db2}")  # Should be True
    
    db1.connect()
    db1.tambah_mahasiswa("2023001", {"nama": "Alice", "jurusan": "TI"})
    db1.tambah_mahasiswa("2023002", {"nama": "Bob", "jurusan": "SI"})
    
    # Akses dari instance kedua
    data_alice = db2.get_mahasiswa("2023001")
    print(f"Data Alice dari db2: {data_alice}")
    
    stats = db1.get_stats()
    print(f"Database stats: {stats}")
    
    db2.disconnect()
    
    print("\n" + "="*80)
    print("📊 RINGKASAN KONSEP OOP PER LEVEL")
    print("="*80)
    
    print("\n📚 LEVEL 1 - BASIC CLASS:")
    print("  ✓ Constructor (__init__)")
    print("  ✓ Instance attributes (self.nama, self.nim)")
    print("  ✓ Instance methods (perkenalan, ubah_jurusan)")
    print("  ✓ Basic object creation")
    
    print("\n💰 LEVEL 2 - CONSTRUCTOR & METHOD:")
    print("  ✓ Default parameters (saldo=0)")
    print("  ✓ Input validation")
    print("  ✓ Return values (True/False)")
    print("  ✓ Error handling")
    print("  ✓ Object interaction (transfer antar akun)")
    
    print("\n👥 LEVEL 3 - INHERITANCE:")
    print("  ✓ Parent class (PersonAkademik)")
    print("  ✓ Child classes (MahasiswaTingkatLanjut, Dosen)")
    print("  ✓ Constructor chaining (super().__init__)")
    print("  ✓ Method overriding (info_dasar)")
    print("  ✓ Method extension dengan super()")
    print("  ✓ Polymorphism")
    
    print("\n🔒 LEVEL 4 - ENCAPSULATION & PROPERTY:")
    print("  ✓ Private attributes (_ipk, _total_sks)")
    print("  ✓ Property decorator (@property)")
    print("  ✓ Getter dan Setter")
    print("  ✓ Data validation dalam setter")
    print("  ✓ Computed properties (status_akademik)")
    print("  ✓ Read-only properties")
    
    print("\n🔧 LEVEL 5 - STATIC & CLASS METHOD:")
    print("  ✓ Static methods (@staticmethod)")
    print("  ✓ Class methods (@classmethod)")
    print("  ✓ Class variables (_skala_nilai)")
    print("  ✓ Utility functions tanpa instance")
    print("  ✓ String parsing dan data processing")
    
    print("\n🏆 LEVEL 6 - ABSTRACT & MULTIPLE INHERITANCE:")
    print("  ✓ Abstract Base Class (ABC)")
    print("  ✓ Abstract methods (@abstractmethod)")
    print("  ✓ Multiple inheritance")
    print("  ✓ Mixin classes (Penelitian, Organisasi)")
    print("  ✓ Method Resolution Order (MRO)")
    print("  ✓ Complex object composition")
    
    print("\n🔄 BONUS - DESIGN PATTERN:")
    print("  ✓ Singleton pattern")
    print("  ✓ __new__ method override")
    print("  ✓ Class-level instance control")
    print("  ✓ State management")
    
    print("\n" + "="*80)
    print("🎯 KOMPLEKSITAS PROGRESSION")
    print("="*80)
    print("Level 1: Dasar OOP → Class sederhana dengan attributes dan methods")
    print("Level 2: Logic → Validasi, error handling, object interaction") 
    print("Level 3: Structure → Hierarchical design dengan inheritance")
    print("Level 4: Security → Data protection dengan encapsulation")
    print("Level 5: Utility → Reusable functions dengan static/class methods")
    print("Level 6: Architecture → Complex design patterns dan multiple inheritance")
    print("Bonus: Advanced → Design patterns untuk real-world applications")


# ===============================
# PERBANDINGAN APPROACH PER LEVEL
# ===============================

def demo_perbandingan_approach():
    print("\n" + "="*80)
    print("🔍 PERBANDINGAN APPROACH: SATU FITUR DI BERBAGAI LEVEL")
    print("="*80)
    
    print("\n📋 STUDI KASUS: Menghitung IPK")
    print("-" * 50)
    
    # Level 1: Basic approach
    print("1️⃣ LEVEL 1 - Basic Class Approach:")
    print("```python")
    print("class MahasiswaBasic:")
    print("    def __init__(self, nama):")
    print("        self.nama = nama")
    print("        self.total_nilai = 0")
    print("        self.total_sks = 0")
    print("    ")
    print("    def hitung_ipk(self):")
    print("        return self.total_nilai / self.total_sks")
    print("```")
    print("❌ Masalah: No validation, bisa error division by zero")
    
    # Level 2: With validation
    print("\n2️⃣ LEVEL 2 - Constructor & Method:")
    print("```python")
    print("def hitung_ipk(self):")
    print("    if self.total_sks == 0:")
    print("        return 0.0")
    print("    return self.total_nilai / self.total_sks")
    print("```")
    print("✅ Perbaikan: Error handling, validation")
    
    # Level 3: Inheritance approach
    print("\n3️⃣ LEVEL 3 - Inheritance:")
    print("```python")
    print("class PersonAkademik:")
    print("    def info_dasar(self): pass")
    print("    ")
    print("class MahasiswaLanjut(PersonAkademik):")
    print("    def hitung_ipk(self): # Override atau extend")
    print("```")
    print("✅ Perbaikan: Reusable structure, polymorphism")
    
    # Level 4: Encapsulation
    print("\n4️⃣ LEVEL 4 - Encapsulation:")
    print("```python")
    print("@property")
    print("def ipk(self):")
    print("    return self._ipk  # Read-only")
    print("    ")
    print("def tambah_nilai(self, nilai, sks):")
    print("    # Automatic recalculation")
    print("    self._ipk = self._calculate_ipk()")
    print("```")
    print("✅ Perbaikan: Data protection, automatic calculation")
    
    # Level 5: Static method
    print("\n5️⃣ LEVEL 5 - Static Method:")
    print("```python")
    print("@staticmethod")
    print("def hitung_ipk(daftar_nilai_sks):")
    print("    # Pure function, no instance needed")
    print("    # Reusable across different contexts")
    print("```")
    print("✅ Perbaikan: Utility function, independent dari instance")
    
    # Level 6: Complex integration
    print("\n6️⃣ LEVEL 6 - Abstract & Multiple Inheritance:")
    print("```python")
    print("class AktivitasAkademik(ABC):")
    print("    @abstractmethod")
    print("    def evaluate_performance(self): pass")
    print("    ")
    print("class MahasiswaAktif(Aktivitas, Penelitian, Organisasi):")
    print("    def evaluate_performance(self):")
    print("        # Gabungan IPK + penelitian + organisasi")
    print("```")
    print("✅ Perbaikan: Holistic evaluation, complex behavior")

    print("\n" + "="*80)
    print("💡 KAPAN MENGGUNAKAN LEVEL MANA?")
    print("="*80)
    
    scenarios = [
        ("Tugas Kuliah Sederhana", "Level 1-2", "Basic class dengan validation"),
        ("Sistem Kecil (< 5 class)", "Level 2-3", "Method kompleks + inheritance"),
        ("Aplikasi Menengah", "Level 3-4", "Inheritance + encapsulation"),
        ("Library/Framework", "Level 4-5", "Property + static/class methods"),
        ("Enterprise Application", "Level 5-6", "Full OOP + design patterns"),
        ("Production System", "Level 6 + Bonus", "Abstract class + patterns")
    ]
    
    for scenario, level, desc in scenarios:
        print(f"📌 {scenario:25} → {level:15} ({desc})")
    
    print("\n" + "="*80)
    print("⚡ PERFORMANCE & COMPLEXITY TRADE-OFF")
    print("="*80)
    
    tradeoffs = [
        ("Level 1", "🚀 Fast", "⚠️ Tidak Scalable", "Prototype/Learning"),
        ("Level 2", "🏃 Good", "✅ Reliable", "Small Projects"),  
        ("Level 3", "🚶 Moderate", "✅ Maintainable", "Medium Projects"),
        ("Level 4", "🐌 Slower", "🔒 Secure", "Data-Critical Apps"),
        ("Level 5", "⚡ Efficient", "🔧 Reusable", "Utility Libraries"),
        ("Level 6", "🎯 Complex", "🏗️ Extensible", "Large Systems")
    ]
    
    print("Level    | Performance | Quality      | Use Case")
    print("-" * 55)
    for level, perf, qual, use in tradeoffs:
        print(f"{level:8} | {perf:11} | {qual:12} | {use}")


# Run the complete demo
if __name__ == "__main__":
    demo_sistem_mahasiswa()
    demo_perbandingan_approach()
    
    print("\n" + "="*80)
    print("🎓 SELESAI! Anda telah melihat 6 level kesulitan OOP dalam satu domain")
    print("="*80)