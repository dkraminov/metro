# -*- coding: utf-8 -*-
import math
import collections
import json
import os


def distance(llat1, llong1, llat2, llong2):
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * 6372795
    return dist


def json_repr(obj, indent=None):
    def serialize(obj):
        # if isinstance(obj, (bool, int, long, float, basestring)):
        if isinstance(obj, (bool, int, float, str)):
            return obj
        elif isinstance(obj, dict):
            obj = obj.copy()
            for key in obj:
                obj[key] = serialize(obj[key])
            return obj
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(serialize([item for item in obj]))
        elif hasattr(obj, '__dict__'):
            return serialize(obj.__dict__)
        else:
            return repr(obj)
    return json.dumps(serialize(obj), indent=indent)


class BasicObj(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class MetroStation(BasicObj):
    def __init__(self, id, name, x, y, lat, lon):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.lat = lat
        self.lon = lon


class MetroLine(BasicObj):
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color
        self.stations = collections.OrderedDict()

    def AddStation(self, id, name, x, y, lat, lon):
        self.stations[id] = MetroStation(id, name, x, y, lat, lon)
        return self.stations[id]


class Metro(BasicObj):
    def __init__(self, id, name, accusative_name):
        self.id = id
        self.name = name
        self.accusative_name = accusative_name
        self.lines = collections.OrderedDict()
        self.times = {}
        self.changes = {}
        self.station_count = 0

    def __SearchStation(self, id):
        for line_id in self.lines:
            line = self.lines[line_id]
            for station_id in line.stations:
                if station_id == id:
                    return line.stations[station_id]
        print("Cant find station '{}'. Halt.".format(id))
        return False

    def FillDefaultTimes(self, metrospeed=41):
        for line_id in self.lines:
            line = self.lines[line_id]
            self.station_count += len(line.stations)
            tmp = line.stations.copy()
            st1 = tmp.popitem()
            while len(tmp):
                st2 = tmp.popitem()
                self.AddTime(st1[1].id, st2[1].id, metrospeed)
                st1 = st2

    def AddLine(self, id, name, color):
        self.lines[id] = MetroLine(id, name, color)
        return self.lines[id]

    def AddTime(self, st1, st2, metrospeed=41):
        st1 = self.__SearchStation(st1)
        st2 = self.__SearchStation(st2)
        time = int(round(distance(st1.lat, st1.lon, st2.lat, st2.lon) / (metrospeed * 1000) * 60 * 60 / 10) * 10)
        self.times["{}@{}".format(st1.id, st2.id)] = time
        self.times["{}@{}".format(st2.id, st1.id)] = time

    def AddChange(self, st1, st2, time=180):
        st1 = self.__SearchStation(st1)
        st2 = self.__SearchStation(st2)
        self.changes["{}@{}".format(st1.id, st2.id)] = time
        self.changes["{}@{}".format(st2.id, st1.id)] = time

samara = Metro('samara', 'Самара', 'Самары')
line = samara.AddLine('pervaya_liniya', 'Первая линия', "ed1c24")
line.AddStation("rossiiskaya", "Российская", 8, 7, 53.2118766980059, 50.1486386614009)
line.AddStation("moskovskaya", "Московская", 8, 29, 53.202790718652, 50.1600313758649)
line.AddStation("gagarinskaya", "Гагаринская", 8, 52, 53.200161337646, 50.177529740611)
line.AddStation("sportivnaya", "Спортивная", 8, 75, 53.2008134491243, 50.2000559364409)
line.AddStation("sovetskaya", "Советская", 8, 97, 53.201480283487, 50.2221422298796)
line.AddStation("pobeda", "Победа", 8, 120, 53.2064477372389, 50.2340666349211)
line.AddStation("bezimyanka", "Безымянка", 26, 142, 53.2125790564215, 50.2474971586028)
line.AddStation("kirovskaya", "Кировская", 26, 164, 53.2108054795459, 50.2705860183973)
line.AddStation("ungorodok", "Юнгородок", 26, 188, 53.2122381393962, 50.2818923630551)
samara.FillDefaultTimes()
print("Samara, {} stations".format(samara.station_count))

novosib = Metro('novosibirsk', 'Новосибирск', 'Новосибирска')
line1 = novosib.AddLine('leninskaya_liniya', 'Ленинская линия', 'ed1c24')
line1.AddStation("zaelcovskaya", "Заельцовская", 139, 5, 55.0594091622915, 82.9125204381385)
line1.AddStation("gagarinskaya", "Гагаринская", 139, 29, 55.051226323532, 82.9147689422392)
line1.AddStation("krasnii_prospekt", "Красный Проспект", 139, 55, 55.0411052276485, 82.9174688526098)
line1.AddStation("ploshad_lenina", "Площадь Ленина", 158, 73, 55.0301250810717, 82.9204697589818)
line1.AddStation("oktyabrskaya", "Октябрьская", 173, 89, 55.0188557871026, 82.9391369750285)
line1.AddStation("rechnoi_vokzal", "Речной Вокзал", 173, 113, 55.008793196091, 82.9383837271621)
line1.AddStation("stydencheskaya", "Студенческая", 158, 128, 54.9892694136023, 82.9066422033525)
line1.AddStation("ploshad_marksa", "Площадь Маркса", 139, 144, 54.9830484136531, 82.8932359733294)
line2 = novosib.AddLine('dzerzhinskaya_liniya', 'Дзержинская линия', '009854')
line2.AddStation("ploshad_garina-mihailovskogo", "Площадь Гарина-Михайловского", 108, 86, 55.0354295741637, 82.898965086287)
line2.AddStation("sibirskaya", "Сибирская", 127, 66, 55.0422949381159, 82.9190003344673)
line2.AddStation("marshala_pokrishkina", "Маршала Покрышкина", 171, 54, 55.0437475829323, 82.9355341205781)
line2.AddStation("berezovaya_rosha", "Березовая Роща", 196, 54, 55.0432446458796, 82.9533895291642)
line2.AddStation("zolotaya_niva", "Золотая Нива", 221, 54, 55.03714, 82.976991)
novosib.AddChange('krasnii_prospekt', 'sibirskaya', 180)
novosib.FillDefaultTimes()
print("Novosib, {} stations".format(novosib.station_count))

kazan = Metro('kazan', 'Казань', 'Казани')
line = kazan.AddLine('centralnaya_liniya', 'Центральная линия', '009854')
line.AddStation("kozya_sloboda", "Козья Слобода", 7, 8, 55.8176094498771, 49.0976540733133)
line.AddStation("kremlevskaya", "Кремлевская", 7, 29, 55.7951938070189, 49.1073671253623)
line.AddStation("ploshad_tykaya", "Площадь Тукая", 7, 53, 55.7871438715778, 49.1220820946131)
line.AddStation("sykonnaya_cloboda", "Суконная Cлобода", 25, 74, 55.7763308530671, 49.1437398340866)
line.AddStation("ametevo", "Аметьево", 25, 96, 55.7651798821464, 49.1664816922534)
line.AddStation("gorki", "Горки", 25, 120, 55.7602495334154, 49.1903547256175)
line.AddStation("prospekt_pobedi", "Проспект Победы", 25, 141, 55.7499520906488, 49.2085103667662)
kazan.FillDefaultTimes()
print("Kazan, {} stations".format(kazan.station_count))

eburg = Metro('eburg', 'Екатеринбург', 'Екатеринбурга')
line = eburg.AddLine('uralskaya_liniya', 'Уральская линия', '009854')
line.AddStation("prospekt_kosmonavtov", "Проспект космонавтов", 44, 8, 56.9024616368319, 60.6134261894226)
line.AddStation("yralmash", "Уралмаш", 44, 33, 56.888682263425, 60.6138774571644)
line.AddStation("mashinostroitelei", "Машиностроителей", 44, 59, 56.8775244683109, 60.6118192056905)
line.AddStation("yralskaya", "Уральская", 8, 95, 56.8580257019274, 60.600102521242)
line.AddStation("dinamo", "Динамо", 8, 117, 56.8478902106605, 60.5994760666923)
line.AddStation("ploshad_1905_goda", "Площадь 1905 года", 8, 140, 56.8362942109837, 60.5997617459885)
line.AddStation("geologicheskaya", "Геологическая", 8, 163, 56.82744226647, 60.603072576321)
line.AddStation("botanicheskaya", "Ботаническая", 8, 186, 56.797778, 60.630833)
eburg.FillDefaultTimes(43)
print("Eburg, {} stations".format(eburg.station_count))

nn = Metro('nn', 'Нижний Новгород', 'Нижнего Новогорода')
line1 = nn.AddLine('avtozavodskaya_liniya', 'Автозаводская линия', 'ed1c24')
line1.AddStation("gorkovskaya", "Горьковская", 157, 31, 56.313889, 43.995)
line1.AddStation("moskovskaya_kr", "Московская (Красная)", 157, 84, 56.3213240515983, 43.9455284486623)
line1.AddStation("chkalovskaya", "Чкаловская", 157, 112, 56.3124761994768, 43.9371058153095)
line1.AddStation("leninskaya", "Ленинская", 157, 137, 56.2977987400589, 43.937914715027)
line1.AddStation("zarechnaya", "Заречная", 157, 162, 56.2851112671261, 43.9270312139491)
line1.AddStation("dvigatel_revolucii", "Двигатель Революции", 157, 189, 56.276490975699, 43.9203733595221)
line1.AddStation("proletarskaya", "Пролетарская", 157, 216, 56.266150483714, 43.9120550675397)
line1.AddStation("avtozavodskaya", "Автозаводская", 157, 244, 56.2579069316524, 43.9025912143989)
line1.AddStation("komsomolskaya", "Комсомольская", 136, 265, 56.2526413933239, 43.8910191643904)
line1.AddStation("kirovskaya", "Кировская", 115, 286, 56.2480548868575, 43.8785797130432)
line1.AddStation("park_kyltyri", "Парк Культуры", 94, 307, 56.2420431826785, 43.8579759272493)
line2 = nn.AddLine('sormovskaya_liniya', 'Сормовская линия', '009854')
line2.AddStation("byrevestnik", "Буревестник", 30, 107, 56.333299270711, 43.8966852693099)
line2.AddStation("byrnakovskaya", "Бурнаковская", 68, 107, 56.3255896320251, 43.9131787704174)
line2.AddStation("kanavinskaya", "Канавинская", 108, 107, 56.3203357436521, 43.9277911365766)
line2.AddStation("moskovskaya_zel", "Московская (Зеленая)", 157, 61, 56.3213240515983, 43.9455284486623)
nn.AddChange('moskovskaya_kr', 'moskovskaya_zel', 100)
nn.FillDefaultTimes(43)
print("NN, {} stations".format(nn.station_count))

piter = Metro("piter", "Санкт-Петербург", 'Санкт-Петербурга')
line = piter.AddLine('kirov', 'Кировско-Выборгская линия', 'ed1c24')
line.AddStation("devyatkino", "Девяткино", 381, 8, 60.0504180568076, 30.4426482418862)
line.AddStation("grajdanskii_prospekt", "Гражданский Проспект", 381, 36, 60.0349932339094, 30.4182351330508)
line.AddStation("akademicheskaya", "Академическая", 381, 64, 60.0127881265531, 30.3959963490528)
line.AddStation("politehnicheskaya", "Политехническая", 381, 93, 60.0089307437261, 30.3708935032768)
line.AddStation("ploshad_myjestva", "Площадь Мужества", 381, 122, 60.0000469062996, 30.3661435100916)
line.AddStation("lesnaya", "Лесная", 381, 149, 59.9847995941546, 30.3442441560376)
line.AddStation("viborgskaya", "Выборгская", 381, 180, 59.97107418397, 30.3473159496264)
line.AddStation("ploshad_lenina", "Площадь Ленина", 381, 211, 59.9587257590329, 30.355063995034)
line.AddStation("chernishevskaya", "Чернышевская", 381, 245, 59.9445719014503, 30.3598681075581)
line.AddStation("ploshad_vosstaniya", "Площадь Восстания", 381, 295, 59.9315704824326, 30.3606049263834)
line.AddStation("vladimirskaya", "Владимирская", 317, 383, 59.9275343978482, 30.3479808584615)
line.AddStation("pyshkinskaya", "Пушкинская", 302, 492, 59.9206848642178, 30.3296434981144)
line.AddStation("tehnologicheskii_instityt_kvl", "Технологический Институт (Красная)", 218, 493, 59.9166016788181, 30.3186305982738)
line.AddStation("baltiiskaya", "Балтийская", 75, 572, 59.9072580709679, 30.2996015594246)
line.AddStation("narvskaya", "Нарвская", 75, 600, 59.9011809354463, 30.2748827438217)
line.AddStation("kirovskii_zavod", "Кировский Завод", 75, 628, 59.8797733555588, 30.2620595696605)
line.AddStation("avtovo", "Автово", 75, 656, 59.8672788214587, 30.2614345671433)
line.AddStation("leninskii_prospekt", "Ленинский Проспект", 75, 686, 59.8516788869126, 30.2695808723803)
line.AddStation("prospekt_veteranov", "Проспект Ветеранов", 75, 713, 59.8422227734773, 30.2500032516966)
line = piter.AddLine('nevsk', 'Невско-Василеостровская линия', '009854')
line.AddStation("primorskaya", "Приморская", 21, 296, 59.9484752058613, 30.2345274705924)
line.AddStation("vasileostrovskaya", "Василеостровская", 41, 317, 59.9426167522675, 30.278239699514)
line.AddStation("gostinii_dvor", "Гостиный Двор", 218, 317, 59.9339491454113, 30.3337259470064)
line.AddStation("mayakovskaya", "Маяковская", 381, 317, 59.931561315709, 30.3549957974087)
line.AddStation("ploshad_aleksandra_nevskogo_nevsk", "Площадь Александра Невского (Зеленая)", 508, 397, 59.9243416529627, 30.3852983081924)
line.AddStation("elizarovskaya", "Елизаровская", 563, 487, 59.8968167794162, 30.4236569405928)
line.AddStation("lomonosovskaya", "Ломоносовская", 563, 515, 59.8773304813072, 30.4417232344821)
line.AddStation("proletarskaya", "Пролетарская", 563, 545, 59.8651930135168, 30.4702524533918)
line.AddStation("obyhovo", "Обухово", 563, 572, 59.8487292712688, 30.4576875846492)
line.AddStation("ribackoe", "Рыбацкое", 563, 603, 59.830908857392, 30.5003616565431)
line = piter.AddLine('mosk', 'Московско-Петроградская линия', '009ddd')
line.AddStation("parnas", "Парнас", 217, 42, 60.0670232650606, 30.3340196112187)
line.AddStation("prospekt_prosvesheniya", "Проспект Просвещения", 217, 70, 60.0514455797832, 30.3324767465782)
line.AddStation("ozerki", "Озерки", 217, 98, 60.0372656165281, 30.3215674601989)
line.AddStation("ydelnaya", "Удельная", 217, 126, 60.0167022808087, 30.3156869293279)
line.AddStation("pionerskaya", "Пионерская", 217, 156, 60.0025163655407, 30.2965246755954)
line.AddStation("chernaya_rechka", "Черная Речка", 217, 183, 59.9854524583016, 30.3008006357264)
line.AddStation("petrogradskaya", "Петроградская", 217, 213, 59.9664767135179, 30.3113497958292)
line.AddStation("gorkovskaya", "Горьковская", 217, 245, 59.9561900629784, 30.3189073644837)
line.AddStation("nevskii_prospekt", "Невский Проспект", 217, 295, 59.9355332422045, 30.3269963086294)
line.AddStation("sennaya_ploshad", "Сенная Площадь", 217, 415, 59.9270433202057, 30.3204448399332)
line.AddStation("tehnologicheskii_instityt_mosk", "Технологический Институт (Синяя)", 217, 516, 59.9166016788181, 30.3186305982738)
line.AddStation("frynzenskaya", "Фрунзенская", 217, 572, 59.906319642133, 30.3174935700306)
line.AddStation("moskovskie_vorota", "Московские Ворота", 217, 600, 59.8917902318199, 30.3176102163092)
line.AddStation("elektrosila", "Электросила", 217, 628, 59.8792808010769, 30.3186513405386)
line.AddStation("park_pobedi", "Парк Победы", 217, 657, 59.866344974198, 30.3219209249361)
line.AddStation("moskovskaya", "Московская", 217, 686, 59.8494055803501, 30.3220888480257)
line.AddStation("zvyozdnaya", "Звёздная", 217, 713, 59.8332655783742, 30.3494755745893)
line.AddStation("kypchino", "Купчино", 217, 744, 59.8295129551429, 30.3755091810098)
line = piter.AddLine('prav', 'Правобережная линия', 'fbaa34')
line.AddStation("spasskaya", "Спасская", 229, 397, 59.9269996463036, 30.3203008931054)
line.AddStation("dostoevskaya", "Достоевская", 302, 397, 59.9283354981234, 30.3460606789687)
line.AddStation("ligovskii_prospekt", "Лиговский Проспект", 381, 397, 59.9208282373637, 30.354986201418)
line.AddStation("ploshad_aleksandra_nevskogo_prav", "Площадь Александра Невского (Желтая)", 486, 397, 59.9236214294491, 30.3834814339649)
line.AddStation("novocherkasskaya", "Новочеркасская", 635, 488, 59.928983338843, 30.4118859995645)
line.AddStation("ladojskaya", "Ладожская", 635, 515, 59.9325178542861, 30.4393841377987)
line.AddStation("prospekt_bolshevikov", "Проспект Большевиков", 635, 544, 59.9199509754615, 30.4668255493613)
line.AddStation("ylica_dibenko", "Улица Дыбенко", 635, 572, 59.9074689860044, 30.4833384194591)
line = piter.AddLine('frun', 'Фрунзенско-Приморская линия', 'b41e8e')
line.AddStation("komendantskii_prospekt", "Комендантский Проспект", 77, 131, 60.0076190963011, 30.2596873508359)
line.AddStation("staraya_derevnya", "Старая Деревня", 77, 160, 59.9892698422187, 30.2551672192333)
line.AddStation("krestovskii_ostrov", "Крестовский Остров", 77, 188, 59.9718506698449, 30.2596895969158)
line.AddStation("chkalovskaya", "Чкаловская", 77, 218, 59.9610021114192, 30.2919371891426)
line.AddStation("sportivnaya", "Спортивная", 77, 245, 59.9521996775544, 30.2914243907198)
line.AddStation("admiralteyskaya", "Адмиралтейская", 163, 352, 59.935579, 30.315685)
line.AddStation("sadovaya", "Садовая", 208, 397, 59.9265460035387, 30.3176918896198)
line.AddStation("zvenigorodskaya", "Звенигородская", 287, 477, 59.922360424689, 30.3356744351351)
line.AddStation("obvodyi_kanal", "Обводный Канал", 379, 596, 59.914571, 30.349632)
line.AddStation("volkovskaya", "Волковская", 379, 624, 59.8960957956714, 30.3574116322867)
line.AddStation("buharestskaya", "Бухарестская", 379, 652, 59.883611, 30.369444)
line.AddStation("mejdynarodnaya", "Международная", 379, 680, 59.87, 30.379722)
piter.AddChange('gostinii_dvor', 'nevskii_prospekt', 180)
piter.AddChange('mayakovskaya', 'ploshad_vosstaniya', 180)
piter.AddChange('ploshad_aleksandra_nevskogo_nevsk', 'ploshad_aleksandra_nevskogo_prav', 180)
piter.AddChange('sadovaya', 'sennaya_ploshad', 180)
piter.AddChange('sadovaya', 'spasskaya', 180)
piter.AddChange('spasskaya', 'sennaya_ploshad', 180)
piter.AddChange('dostoevskaya', 'vladimirskaya', 180)
piter.AddChange('tehnologicheskii_instityt_kvl', 'tehnologicheskii_instityt_mosk', 180)
piter.AddChange('zvenigorodskaya', 'pyshkinskaya', 180)
piter.FillDefaultTimes(39)
print("Piter, {} stations".format(piter.station_count))

moscow = Metro("moscow", "Москва", 'Москвы')
line = moscow.AddLine('sokolnicheskaya_liniya', 'Сокольническая линия', 'ed1c24')
line.AddStation("ylica_podbelskogo", "Улица Подбельского", 607, 132, 55.8145329646495, 37.7337504744297)
line.AddStation("cherkizovskaya", "Черкизовская", 607, 161, 55.8032729351313, 37.7467170092299)
line.AddStation("preobrajenskaya_ploshad", "Преображенская площадь", 587, 178, 55.796157889621, 37.7152449519615)
line.AddStation("sokolniki", "Сокольники", 568, 197, 55.7892616354543, 37.6797138681324)
line.AddStation("krasnoselskaya", "Красносельская", 549, 215, 55.7801174241401, 37.6662874401897)
line.AddStation("komsomolskaya_kr", "Комсомольская", 513, 252, 55.7749893674483, 37.6560826055666)
line.AddStation("krasnie_vorota", "Красные ворота", 474, 271, 55.7688791370204, 37.6490966134596)
line.AddStation("chistie_prydi", "Чистые пруды", 453, 289, 55.7652821242466, 37.6384808002614)
line.AddStation("lybyanka", "Лубянка", 408, 337, 55.7601546540212, 37.625874958665)
line.AddStation("ohotnii_ryad", "Охотный ряд", 375, 370, 55.7572501447119, 37.6173166444836)
line.AddStation("biblioteka_im_lenina", "Библиотека им. Ленина", 343, 400, 55.7526999768777, 37.6109992836521)
line.AddStation("kropotkinskaya", "Кропоткинская", 286, 457, 55.7451439240646, 37.602783501042)
line.AddStation("park_kyltyri_kr", "Парк культуры", 265, 479, 55.7358450335055, 37.5945073381868)
line.AddStation("frynzenskaya", "Фрунзенская", 251, 538, 55.727610079947, 37.5802236295585)
line.AddStation("sportivnaya", "Спортивная", 227, 561, 55.7231139316859, 37.5639696522489)
line.AddStation("vorobevi_gori", "Воробьевы горы", 199, 589, 55.7102488315714, 37.5591435377664)
line.AddStation("yniversitet", "Университет", 177, 612, 55.69259362805, 37.5346727455108)
line.AddStation("prospekt_vernadskogo", "Проспект Вернадского", 153, 635, 55.6769473973178, 37.5060930792933)
line.AddStation("ugo-zapadnaya", "Юго-Западная", 153, 663, 55.6637734696351, 37.4833195605717)
line = moscow.AddLine('zamoskvoretskaya_liniya', 'Замоскворецкая линия', '009854')
line.AddStation("rechnoi_vokzal", "Речной вокзал", 188, 117, 55.8550927177238, 37.4763584047788)
line.AddStation("vodnii_stadion", "Водный стадион", 188, 138, 55.8398451032555, 37.4871323722088)
line.AddStation("voikovskaya", "Войковская", 188, 160, 55.8189257050376, 37.4977968171355)
line.AddStation("sokol", "Сокол", 188, 184, 55.8049957790759, 37.5149771624959)
line.AddStation("aeroport", "Аэропорт", 206, 201, 55.8008145135566, 37.5337097532744)
line.AddStation("dinamo", "Динамо", 222, 218, 55.7898210936147, 37.5582326851342)
line.AddStation("belorysskaya_zel", "Белорусская", 242, 237, 55.7765968858362, 37.5818786248922)
line.AddStation("mayakovskaya", "Маяковская", 290, 286, 55.7694362254521, 37.5970093823579)
line.AddStation("tverskaya", "Тверская", 338, 334, 55.7662652339699, 37.6052272386422)
line.AddStation("teatralnaya", "Театральная", 389, 384, 55.7574096283081, 37.6188362564546)
line.AddStation("novokyzneckaya", "Новокузнецкая", 389, 496, 55.7421341339971, 37.629594333576)
line.AddStation("paveleckaya_zel", "Павелецкая", 434, 557, 55.729768818076, 37.6387625110374)
line.AddStation("avtozavodskaya", "Автозаводская", 477, 601, 55.7071696324186, 37.6574458018926)
line.AddStation("kolomenskaya", "Коломенская", 477, 651, 55.6783911195916, 37.6638941121713)
line.AddStation("kashirskaya_zel", "Каширская", 477, 675, 55.6550875439577, 37.6490661704077)
line.AddStation("kantemirovskaya", "Кантемировская", 477, 700, 55.6357865840338, 37.6566178650091)
line.AddStation("caricino", "Царицыно", 494, 717, 55.6216590185028, 37.6701430514343)
line.AddStation("orehovo", "Орехово", 512, 734, 55.6134990126532, 37.695685175318)
line.AddStation("domodedovskaya", "Домодедовская", 529, 752, 55.6109583130938, 37.7195988327795)
line.AddStation("krasnogvardeiskaya", "Красногвардейская", 546, 770, 55.6140481939377, 37.7445232639254)
line.AddStation("almaatinskaya", "Алма-Атинская", 546, 795, 55.633475, 37.765633)
line = moscow.AddLine('arbatsko-pokrovskaya_liniya', 'Арбатско-Покровcкая линия', '00539f')
line.AddStation("shelkovskaya", "Щелковская", 627, 235, 55.8109250841654, 37.7985452142914)
line.AddStation("pervomaiskaya", "Первомайская", 627, 260, 55.7945545415907, 37.7993616275653)
line.AddStation("izmailovskaya", "Измайловская", 627, 284, 55.7876821076541, 37.7813865037381)
line.AddStation("partizanskaya", "Партизанская", 627, 309, 55.7875765833999, 37.7486826814915)
line.AddStation("semenovskaya", "Семеновская", 627, 338, 55.7832720937083, 37.7196988148305)
line.AddStation("elektrozavodskaya", "Электрозаводская", 610, 356, 55.7822190260863, 37.7066890012092)
line.AddStation("baymanskaya", "Бауманская", 592, 374, 55.772472556937, 37.6795233027091)
line.AddStation("kyrskaya_sin", "Курская", 565, 399, 55.7582621743204, 37.6593339903959)
line.AddStation("ploshad_revolucii", "Площадь Революции", 404, 400, 55.756922144145, 37.6226743592945)
line.AddStation("arbatskaya_sin", "Арбатская", 313, 400, 55.7518377582274, 37.6040132591889)
line.AddStation("smolenskaya_sin", "Смоленская", 270, 400, 55.7480073145646, 37.5836861467845)
line.AddStation("kievskaya_sin", "Киевская", 206, 465, 55.7438910408958, 37.5672933836518)
line.AddStation("park_pobedi", "Парк Победы", 111, 457, 55.7364409961909, 37.5146793512337)
line.AddStation("slavyanskii_bylvar", "Славянский бульвар", 75, 421, 55.7295226943314, 37.4711104411516)
line.AddStation("kyncevskaya_sin", "Кунцевская", 27, 370, 55.7307221435719, 37.446058754626)
line.AddStation("molodejnaya", "Молодежная", 27, 335, 55.7409136609931, 37.4170590628804)
line.AddStation("krilatskoe", "Крылатское", 27, 313, 55.7568639356345, 37.4081355232734)
line.AddStation("strogino", "Строгино", 27, 246, 55.803784089029, 37.4025417480209)
line.AddStation("myakinino", "Мякинино", 27, 209, 55.8249368342387, 37.3852176055605)
line.AddStation("volokolamskaya", "Волоколамская", 27, 173, 55.8351578497631, 37.3825827972405)
line.AddStation("mitino", "Митино", 27, 139, 55.8455902246608, 37.3625852786958)
line.AddStation("pyatnitskoe_shosse", "Пятницкое шоссе", 27, 105, 55.853634, 37.353108)
line = moscow.AddLine('filevskaya_liniya', 'Филевская линия', '009ddd')
line.AddStation("kyncevskaya_fil", "Кунцевская (Филевская)", 49, 371, 55.7307954112642, 37.446009616004)
line.AddStation("pionerskaya", "Пионерская", 67, 391, 55.7360278873923, 37.4671169547887)
line.AddStation("filevskii_park", "Филевский парк", 83, 406, 55.7395539460918, 37.4833361280302)
line.AddStation("bagrationovskaya", "Багратионовская", 98, 421, 55.7437379883965, 37.4977188191092)
line.AddStation("fili", "Фили", 113, 437, 55.7461114404983, 37.5149309519302)
line.AddStation("kytyzovskaya", "Кутузовская", 127, 451, 55.7399662088372, 37.5341798748651)
line.AddStation("stydencheskaya", "Студенческая", 159, 483, 55.7386877747795, 37.5484841803272)
line.AddStation("kievskaya_fil", "Киевская (Филевская)", 207, 436, 55.7441618474204, 37.5669310769079)
line.AddStation("smolenskaya_fil", "Смоленская (Филевская)", 257, 387, 55.7493950652958, 37.5824093057416)
line.AddStation("arbatskaya_fil", "Арбатская (Филевская)", 300, 387, 55.7524068663913, 37.6017552028193)
line.AddStation("aleksandrovskii_sad", "Александровский сад", 328, 387, 55.7523004876049, 37.6100102730035)
line = moscow.AddLine('kolcevaya_liniya', 'Кольцевая линия', '745d32')
line.AddStation("paveleckaya_kl", "Павелецкая (Кольцевая)", 435, 537, 55.7316074402358, 37.6373390451641)
line.AddStation("dobrininskaya", "Добрынинская", 401, 546, 55.7290611864152, 37.622594039598)
line.AddStation("oktyabrskaya_kl", "Октябрьская (Кольцевая)", 327, 539, 55.7292579502018, 37.6112267797669)
line.AddStation("park_kyltyri_kl", "Парк культуры (Кольцевая)", 251, 494, 55.7353776705526, 37.5936679167637)
line.AddStation("kievskaya_kl", "Киевская (Кольцевая)", 221, 451, 55.7446816616271, 37.5673195392161)
line.AddStation("krasnopresnenskaya", "Краснопресненская", 209, 338, 55.7605982500654, 37.5775481554019)
line.AddStation("belorysskaya_kl", "Белорусская (Кольцевая)", 258, 253, 55.7757189562805, 37.5822436892428)
line.AddStation("novoslobodskaya", "Новослободская", 331, 210, 55.7797079127576, 37.6015092940327)
line.AddStation("prospekt_mira_kl", "Проспект Мира (Кольцевая)", 455, 225, 55.7798527191266, 37.6336962175341)
line.AddStation("komsomolskaya_kl", "Комсомольская (Кольцевая)", 493, 253, 55.7746613830448, 37.6560374272919)
line.AddStation("kyrskaya_kl", "Курская (Кольцевая)", 545, 400, 55.7581799984773, 37.6599285643101)
line.AddStation("taganskaya_kl", "Таганская (Кольцевая)", 516, 475, 55.742372976687, 37.6534364079968)
line = moscow.AddLine('kaluzhsko-rizhskaya_liniya', 'Калужско-Рижская линия', 'fbaa34')
line.AddStation("medvedkovo", "Медведково", 505, 44, 55.8872198056911, 37.6615705750369)
line.AddStation("babyshkinskaya", "Бабушкинская", 505, 71, 55.8696018716677, 37.6641531729066)
line.AddStation("sviblovo", "Свиблово", 487, 89, 55.8554197738278, 37.6527128696718)
line.AddStation("botanicheskii_sad", "Ботанический сад", 470, 106, 55.8454519850472, 37.6382309091642)
line.AddStation("vdnh", "ВДНХ", 470, 132, 55.8210353720813, 37.6413180391564)
line.AddStation("alekseevskaya", "Алексеевская", 470, 159, 55.8083000661719, 37.638982165517)
line.AddStation("rijskaya", "Рижская", 470, 185, 55.7924140491293, 37.6365694226775)
line.AddStation("prospekt_mira_or", "Проспект Мира", 470, 210, 55.7817711213755, 37.6338226473964)
line.AddStation("syharevskaya", "Сухаревская", 454, 247, 55.772960593943, 37.6327948494404)
line.AddStation("tyrgenevskaya", "Тургеневская", 454, 310, 55.7657173903248, 37.63738786512)
line.AddStation("kitai-gorod_or", "Китай-город (Оранжевая)", 454, 414, 55.7549840759628, 37.632819222501)
line.AddStation("tretyakovskaya_or", "Третьяковская (Оранжевая)", 391, 475, 55.7416720242377, 37.6279852054761)
line.AddStation("oktyabrskaya_or", "Октябрьская", 341, 525, 55.730619218207, 37.6129028251401)
line.AddStation("shabolovskaya", "Шаболовская", 326, 578, 55.7191764230145, 37.6082624863331)
line.AddStation("leninskii_prospekt", "Ленинский проспект", 311, 593, 55.7074958388455, 37.5861632819777)
line.AddStation("akademicheskaya", "Академическая", 295, 609, 55.6878708935511, 37.5735613932869)
line.AddStation("profsouznaya", "Профсоюзная", 279, 625, 55.6779308416232, 37.5628687844352)
line.AddStation("novie_cheremyshki", "Новые Черемушки", 263, 641, 55.6703155517091, 37.5544942666522)
line.AddStation("kalyjskaya", "Калужская", 248, 656, 55.6571347079362, 37.5404968403609)
line.AddStation("belyaevo", "Беляево", 233, 672, 55.6424642181538, 37.5263085205996)
line.AddStation("konkovo", "Коньково", 233, 690, 55.6331135681431, 37.5193657102966)
line.AddStation("teplii_stan", "Теплый Стан", 233, 709, 55.6188296190623, 37.5075130601728)
line.AddStation("yasenevo", "Ясенево", 246, 724, 55.6060873664551, 37.5333097404951)
line.AddStation("novoyasenevskaya", "Новоясеневская", 262, 741, 55.6014443131177, 37.554153269075)
line = moscow.AddLine('tagansko-krasnopresnenskaya_liniya', 'Таганско-Краснопресненская линия', 'b41e8e')
line.AddStation("planernaya", "Планерная", 139, 162, 55.860500801133, 37.4366871384151)
line.AddStation("shodnenskaya", "Сходненская", 139, 189, 55.8504316657611, 37.4398114739516)
line.AddStation("tyshinskaya", "Тушинская", 139, 222, 55.826321232012, 37.4369017630164)
line.AddStation("shykinskaya", "Щукинская", 139, 245, 55.8085514026087, 37.4642174709607)
line.AddStation("oktyabrskoe_pole", "Октябрьское поле", 139, 269, 55.7935072180172, 37.4936084071142)
line.AddStation("polejaevskaya", "Полежаевская", 156, 287, 55.777539362395, 37.5192818481553)
line.AddStation("begovaya", "Беговая", 173, 303, 55.7736864843681, 37.5468261144269)
line.AddStation("ylica_1905_goda", "Улица 1905 года", 190, 320, 55.765053939476, 37.5615752956231)
line.AddStation("barrikadnaya", "Баррикадная", 229, 338, 55.7608035124379, 37.58128813026)
line.AddStation("pyshkinskaya", "Пушкинская", 319, 336, 55.7650697910311, 37.6067526814352)
line.AddStation("kyzneckii_most", "Кузнецкий мост", 424, 353, 55.7612602954786, 37.6249079305951)
line.AddStation("kitai-gorod_vio", "Китай-город (Фиолетовая)", 485, 414, 55.7554003223101, 37.6338310200866)
line.AddStation("taganskaya_vio", "Таганская", 535, 465, 55.739614063447, 37.6530720186384)
line.AddStation("proletarskaya", "Пролетарская", 581, 511, 55.7320223612723, 37.6677944251762)
line.AddStation("volgogradskii_prospekt", "Волгоградский проспект", 610, 540, 55.7252793907609, 37.6865298999307)
line.AddStation("tekstilshiki", "Текстильщики", 628, 558, 55.7092245671963, 37.7313369713417)
line.AddStation("kyzminki", "Кузьминки", 645, 575, 55.7054530174972, 37.7654250647072)
line.AddStation("ryazanskii_prospekt", "Рязанский проспект", 669, 576, 55.7168692271045, 37.7931354761886)
line.AddStation("vihino", "Выхино", 694, 576, 55.7159646023232, 37.8178090012778)
line = moscow.AddLine('kalininskaya_liniya', 'Калининская линия', 'ffd400')
line.AddStation("novokisino", "Новокосино", 698, 392, 55.744708454753, 37.863254775219)
line.AddStation("novogireevo", "Новогиреево", 680, 411, 55.7518688489458, 37.816680546334)
line.AddStation("perovo", "Перово", 660, 429, 55.7511736483108, 37.7863397581296)
line.AddStation("shosse_entyziastov", "Шоссе Энтузиастов", 642, 448, 55.7589012870796, 37.7521507941493)
line.AddStation("aviamotornaya", "Авиамоторная", 623, 467, 55.7515620184703, 37.7170590251201)
line.AddStation("ploshad_ilicha", "Площадь Ильича", 581, 485, 55.7469721149821, 37.6808757142437)
line.AddStation("marksistskaya", "Марксистская", 535, 485, 55.7411431310035, 37.6565777481078)
line.AddStation("tretyakovskaya_zh", "Третьяковская (Желтая)", 409, 485, 55.7411243839815, 37.6291930465031)
line = moscow.AddLine('serpuhovsko-timiryazevskaya_liniya', 'Серпуховско-Тимирязевская линия', 'abadb0')
line.AddStation("altyfevo", "Алтуфьево", 317, 20, 55.8979164889871, 37.587134939137)
line.AddStation("bibirevo", "Бибирево", 333, 37, 55.8842754933877, 37.6026913409615)
line.AddStation("otradnoe", "Отрадное", 333, 59, 55.8633869076221, 37.604850413685)
line.AddStation("vladikino", "Владыкино", 333, 81, 55.8472811207559, 37.5898807710529)
line.AddStation("petrovsko-razymovskaya", "Петровско-Разумовская", 317, 96, 55.8360431202466, 37.5748440790378)
line.AddStation("timiryazevskaya", "Тимирязевская", 317, 123, 55.8184072151451, 37.5760080037778)
line.AddStation("dmitrovskaya", "Дмитровская", 317, 146, 55.8075474370831, 37.5812008833455)
line.AddStation("savelovskaya", "Савеловская", 317, 175, 55.7935212374439, 37.5883596061548)
line.AddStation("mendeleevskaya", "Менделеевская", 317, 196, 55.7815311525213, 37.5997663021334)
line.AddStation("cvetnoi_bylvar", "Цветной бульвар", 382, 264, 55.7720911430623, 37.6212564818892)
line.AddStation("chehovskaya", "Чеховская", 329, 317, 55.7658078755777, 37.6075290899373)
line.AddStation("borovickaya", "Боровицкая", 329, 417, 55.7517062709606, 37.6101586923623)
line.AddStation("polyanka", "Полянка", 338, 481, 55.7368034041058, 37.6192178437938)
line.AddStation("serpyhovskaya", "Серпуховская", 402, 567, 55.7269307330764, 37.6242187373292)
line.AddStation("tylskaya", "Тульская", 402, 593, 55.7087409219019, 37.6226752963429)
line.AddStation("nagatinskaya", "Нагатинская", 402, 616, 55.6831642634546, 37.6221337765917)
line.AddStation("nagornaya", "Нагорная", 379, 639, 55.673227649678, 37.6111284544944)
line.AddStation("nahimovskii_prospekt", "Нахимовский проспект", 379, 657, 55.6626542521309, 37.6052996623838)
line.AddStation("sevastopolskaya", "Севастопольская", 379, 676, 55.6514310726072, 37.5984807065682)
line.AddStation("chertanovskaya", "Чертановская", 379, 695, 55.641472119368, 37.605941794867)
line.AddStation("ujnaya", "Южная", 397, 713, 55.6223634503418, 37.6086769692483)
line.AddStation("prajskaya", "Пражская", 397, 732, 55.6122405285658, 37.6039809131235)
line.AddStation("ylica_akademika_yangelya", "Улица Академика Янгеля", 397, 750, 55.5955230472478, 37.6008192711872)
line.AddStation("annino", "Аннино", 397, 769, 55.5832532562542, 37.596838703327)
line.AddStation("bylvar_dmitriya_donskogo", "Бульвар Дмитрия Донского", 363, 803, 55.5693873763878, 37.5763692691798)
line = moscow.AddLine('lublinskaya_liniya', 'Люблинская линия', 'b3d335')
line.AddStation("maryina_roscha", "Марьина роща", 403, 159, 55.7957982572654, 37.6155207486221)
line.AddStation("dostoevskaya", "Достоевская", 403, 190, 55.7817420537442, 37.6137439800057)
line.AddStation("trybnaya", "Трубная", 403, 265, 55.7674720681855, 37.6220601686407)
line.AddStation("sretenskii_bylvar", "Сретенский бульвар", 436, 301, 55.766110855008, 37.6358221489846)
line.AddStation("chkalovskaya", "Чкаловская", 556, 418, 55.7568245013459, 37.6591649191067)
line.AddStation("rimskaya", "Римская", 581, 464, 55.7463639025237, 37.6800390212332)
line.AddStation("krestyanskaya_zastava", "Крестьянская застава", 581, 532, 55.7324504713461, 37.6657301592817)
line.AddStation("dybrovka", "Дубровка", 581, 568, 55.7172764783732, 37.6772188529301)
line.AddStation("kojyhovskaya", "Кожуховская", 581, 593, 55.7062054359999, 37.6855970267035)
line.AddStation("pechatniki", "Печатники", 604, 617, 55.6927055116029, 37.7281035384923)
line.AddStation("voljskaya", "Волжская", 626, 640, 55.6907551038044, 37.7528312176472)
line.AddStation("lublino", "Люблино", 626, 657, 55.6757564456767, 37.7614752997209)
line.AddStation("bratislavskaya", "Братиславская", 626, 674, 55.6595003179762, 37.7508088672566)
line.AddStation("marino", "Марьино", 626, 692, 55.6501547737319, 37.743907070821)
line.AddStation("borisovo", "Борисово", 626, 714, 55.632504866956, 37.7432330407045)
line.AddStation("shipilovskaya", "Шипиловская", 589, 751, 55.6212862484532, 37.7435819746988)
line.AddStation("zyablikovo", "Зябликово", 568, 770, 55.6147239432002, 37.746204662916)
line = moscow.AddLine('kahovskaya_liniya', 'Каховская линия', '0092b9')
line.AddStation("kahovskaya", "Каховская", 400, 676, 55.6529984860912, 37.5982901683088)
line.AddStation("varshavskaya", "Варшавская", 430, 676, 55.6534945739882, 37.619564432063)
line.AddStation("kashirskaya_khv", "Каширская (Каховская)", 459, 676, 55.6552429161534, 37.6486914469033)
line = moscow.AddLine('butovskaya_liniya', 'Бутовская линия легкого метро', '8ad7f8')
line.AddStation("starokachalovskaya", "Старокачаловская", 344, 803, 55.5691961577774, 37.5761617824723)
line.AddStation("ylica_skobelevskaya", "Улица Скобелевская", 344, 826, 55.5481532487645, 37.5547695293099)
line.AddStation("bylvar_admirala_yshakova", "Бульвар Адмирала Ушакова", 344, 845, 55.5454191144993, 37.5430516256895)
line.AddStation("ylica_gorchakova", "Улица Горчакова", 344, 865, 55.5417950203364, 37.530787918568)
line.AddStation("byninskaya_alleya", "Бунинская аллея", 366, 865, 55.5381751922768, 37.5165348925232)
# Остальные
moscow.AddChange('chkalovskaya', 'kyrskaya_kl', 180)
moscow.AddChange('chehovskaya', 'pyshkinskaya', 180)
# Арбатско-покровская
moscow.AddChange('kyncevskaya_sin', 'kyncevskaya_fil', 180)
moscow.AddChange('kievskaya_sin', 'kievskaya_fil', 180)
moscow.AddChange('kievskaya_sin', 'kievskaya_kl', 180)
moscow.AddChange('arbatskaya_sin', 'borovickaya', 180)
moscow.AddChange('arbatskaya_sin', 'aleksandrovskii_sad', 180)
moscow.AddChange('arbatskaya_sin', 'biblioteka_im_lenina', 180)
moscow.AddChange('ploshad_revolucii', 'teatralnaya', 180)
moscow.AddChange('kyrskaya_sin', 'kyrskaya_kl', 180)
moscow.AddChange('kyrskaya_sin', 'chkalovskaya', 180)
moscow.AddChange('tretyakovskaya_or', 'tretyakovskaya_zh', 180)
# Сокольническая
moscow.AddChange('komsomolskaya_kr', 'komsomolskaya_kl', 180)
moscow.AddChange('chistie_prydi', 'tyrgenevskaya', 180)
moscow.AddChange('chistie_prydi', 'sretenskii_bylvar', 180)
moscow.AddChange('lybyanka', 'kyzneckii_most', 180)
moscow.AddChange('ohotnii_ryad', 'teatralnaya', 180)
moscow.AddChange('biblioteka_im_lenina', 'borovickaya', 180)
moscow.AddChange('biblioteka_im_lenina', 'aleksandrovskii_sad', 180)
moscow.AddChange('park_kyltyri_kr', 'park_kyltyri_kl', 180)
# Замоскворецкая
moscow.AddChange('belorysskaya_zel', 'belorysskaya_kl', 180)
moscow.AddChange('tverskaya', 'pyshkinskaya', 180)
moscow.AddChange('tverskaya', 'chehovskaya', 180)
moscow.AddChange('novokyzneckaya', 'tretyakovskaya_or', 180)
moscow.AddChange('novokyzneckaya', 'tretyakovskaya_zh', 180)
moscow.AddChange('paveleckaya_zel', 'paveleckaya_kl', 180)
moscow.AddChange('kashirskaya_zel', 'kashirskaya_khv', 180)
moscow.AddChange('krasnogvardeiskaya', 'zyablikovo', 180)
# Филевская
moscow.AddChange('kievskaya_fil', 'kievskaya_kl', 180)
# Калужско-рижская
moscow.AddChange('prospekt_mira_or', 'prospekt_mira_kl', 180)
moscow.AddChange('tyrgenevskaya', 'sretenskii_bylvar', 180)
moscow.AddChange('kitai-gorod_or', 'kitai-gorod_vio', 180)
moscow.AddChange('tretyakovskaya_or', 'tretyakovskaya_zh', 180)
moscow.AddChange('oktyabrskaya_or', 'oktyabrskaya_kl', 180)
# Таганско-краснопресненская
moscow.AddChange('barrikadnaya', 'krasnopresnenskaya', 180)
moscow.AddChange('taganskaya_vio', 'marksistskaya', 180)
moscow.AddChange('taganskaya_vio', 'taganskaya_kl', 180)
moscow.AddChange('proletarskaya', 'krestyanskaya_zastava', 180)
# Калининская
moscow.AddChange('ploshad_ilicha', 'rimskaya', 180)
moscow.AddChange('marksistskaya', 'taganskaya_kl', 180)
# Серпуховская
moscow.AddChange('novoslobodskaya', 'mendeleevskaya', 180)
moscow.AddChange('cvetnoi_bylvar', 'trybnaya', 180)
moscow.AddChange('serpyhovskaya', 'dobrininskaya', 180)
moscow.AddChange('sevastopolskaya', 'kahovskaya', 180)
moscow.AddChange('bylvar_dmitriya_donskogo', 'starokachalovskaya', 180)
moscow.FillDefaultTimes(41.3)
# close ring line
moscow.AddTime('paveleckaya_kl', 'taganskaya_kl')
line = moscow.lines['filevskaya_liniya']
line.AddStation("vistavochnaya", "Выставочная", 159, 388, 55.7501978870751, 37.5427727388134)
line.AddStation("mejdynarodnaya", "Международная", 159, 364, 55.7483038053698, 37.5334603045829)
moscow.AddTime('kievskaya_fil', 'vistavochnaya')
moscow.AddTime('vistavochnaya', 'mejdynarodnaya')
print("Moscow, {} stations".format(moscow.station_count))

try:
    os.mkdir('json')
except:
    pass

open('json/samara.json', 'w').write(json_repr(samara))
open('json/novosib.json', 'w').write(json_repr(novosib))
open('json/kazan.json', 'w').write(json_repr(kazan))
open('json/moscow.json', 'w').write(json_repr(moscow))
open('json/piter.json', 'w').write(json_repr(piter))
open('json/eburg.json', 'w').write(json_repr(eburg))
open('json/nn.json', 'w').write(json_repr(nn))

