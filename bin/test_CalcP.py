from CalcP import *
import py_accessories
from numpy.testing import assert_array_equal, assert_allclose
import pandas as pd
import scipy.stats as ss

def test_empP():

    taus = [0, 1, 0.2, 0.5]
    emps = [0.1, 0.2, 0.3, 0.4, 0.6]

    exp = [ 6.0/6.0, 1/6.0, 5.0/6.0, 2/6.0 ]

    res = empP(taus, emps)

    assert_array_equal(exp, res)


def test_corrections():


    fn_pkl = "./outputs/Py37Input_out_jtknull1000.txt"

    taus = pd.read_table(fn_pkl)['Tau']
    # print("{}".format(taus[0:2]))
    assert len(taus) == 1000

    fit = False

    keys, intvalues, yerr, p0, limit = prepare(taus)
    if fit:
        for _ in range(2):
            params = GammaFit(keys, intvalues, yerr, p0, limit)
            p0 = params[0]
    params = p0

    print("G params: {}",params)
    gd = ss.gamma(params[0], params[1], params[2])

    keys = [0.05, 0.1, 0.2, 0.5, 0.9]
    keys = np.array(list(keys), dtype=float)

    empPs = empP(keys, taus)

    print("EMPP\n{}".format(empPs))
    ps = gd.sf(keys)
    print("GP\n{}".format(ps))
    assert 1 > 2

def test_gamma():

    gD_3_2 = [3.035778503055554, 2.223693770986615, 10.553021157440465, 5.482199625702728, 4.315356080728167, 3.6281758034393246,
     6.870646712665314, 10.48272971594006, 0.7700651730649672, 13.90643921641651, 8.38954730731031, 8.813879449567924,
     14.275832093652621, 6.521388296104927, 5.450052861274725, 2.1104890335575166, 10.02972432258828, 4.100397426051385,
     15.448753675329316, 2.349723689426407, 5.395209152753688, 4.479304081713186, 4.726788122847339, 7.823069297831669,
     5.76885189482954, 6.289786902016086, 2.5513774225956634, 9.812961852420038, 2.868824077879273, 5.752537120897397,
     11.65934864423813, 6.2298649036789175, 6.257874728432412, 2.122564676290328, 3.6108322580843026, 7.3197272754927,
     8.66817681338522, 6.095795517665715, 14.127175614629287, 2.754708197951353, 1.8581039602287093, 6.964622463010514,
     4.860787614180261, 3.057557791521031, 2.594757296039875, 6.72928389285765, 3.7752539092372537, 5.69181530847974,
     3.180262860313871, 3.655899502930559, 6.713020238412473, 3.698578220970533, 6.145917400546221, 5.64035646643131,
     7.108476028906378, 6.103358832413036, 3.3731400082412404, 7.850547841925968, 5.583525685413663, 6.175122423854175,
     4.128935121331885, 5.805817742909725, 3.5311431754047167, 0.7063275389403654, 6.297995047645648, 1.919458986885072,
     4.845540657020317, 5.676066640905118, 2.3691252507412046, 1.6897700708685521, 6.872354821263578, 5.480108314206351,
     4.555432996569779, 6.18053746339975, 3.5039122865971413, 4.074268169818135, 5.914635030570318, 12.056126793130726,
     12.943485840895637, 4.155573766356251, 12.909943629060866, 9.28945337806835, 2.1670146022372174, 9.08615254922945,
     5.1054316031487135, 3.777244427607224, 9.647908375778613, 4.144491293877849, 1.780724293586862, 7.814646325287449,
     2.9514700752467435, 7.0709279127274485, 6.143711867257501, 12.260957248832934, 4.362314798251283,
     3.1613143202013827, 3.117044128624026, 10.876638272446108, 4.224788322441215, 4.308306409144167,
     2.6822397998788277, 12.244552102029752, 17.286124198734, 3.339524680920603, 9.132748369173356, 7.871289893123363,
     8.761779083849394, 5.32830616670136, 10.032159486309348, 3.4572146525734144, 5.376967761793772, 7.551563486232267,
     2.1467615037908265, 4.962345256040743, 2.889692291601222, 7.0193207915101805, 5.907417455319155, 6.111361984470566,
     8.221304738935295, 10.348802801782563, 4.457443720173612, 2.918670819094788, 6.762815307551776, 7.985285178507159,
     4.0919493422039395, 3.3986116793651657, 5.952178111131392, 8.48406771731931, 1.8228230154810232, 5.049423598181903,
     10.447662643507293, 6.7654253829808155, 3.8266787295144984, 2.9392425723912354, 4.048390631749129,
     7.373886683716528, 6.246224052467708, 3.880734935737105, 5.555032717476854, 2.426746623375679, 12.711376368881972,
     11.79267247751297, 14.191186031553231, 10.88370559094726, 1.3502130909776353, 5.922484697637367, 4.87464433174455,
     7.844265303553698, 2.7927895767662836, 8.66806728532952, 7.456753658462863, 6.2073310601140195, 1.1563932270068142,
     8.747113186800782, 4.668719750055811, 7.394938664851722, 2.0975179009968343, 3.8199955912486954, 11.28856132349865,
     5.397871564312879, 7.014484186578647, 3.603378198660375, 5.286930240773229, 3.8816821784623743, 11.02104242331801,
     2.1880530029324126, 6.393766441499296, 4.633753972029664, 9.472296105109972, 8.661388382588436, 9.517623185813637,
     5.9193195418719835, 7.272100194300355, 10.41757657475485, 6.965887576174303, 6.6816307056331405,
     15.903849754234454, 6.455420408902484, 18.128550341328648, 1.9396140436861284, 5.631286544500661,
     2.7545233400441793, 13.737320312230048, 3.325082760319159, 3.714569851409194, 3.537836493988698, 6.943061474515262,
     8.473151379441207, 2.938741725391293, 4.346882401598543, 4.9398367855990895, 9.887177351099881, 6.560404613001234,
     11.566029085246278, 5.653782265511811, 9.511442556120095, 1.5554935130834793, 9.47466046618491, 8.486394837691833,
     3.5872198700944926, 5.660120104328568, 2.6959143161480252, 10.473917143440213, 3.4721968894551702,
     4.290748020630195, 7.573714614230097, 0.40629455805002884, 5.182492081959248, 4.938412777712484,
     10.691196294303793, 7.314056680485742, 9.584029127670398, 7.861616762479921, 4.217283562316126, 4.800193901632097,
     4.642240255623531, 4.622614747542761, 3.124195495702895, 3.799173755921896, 11.002253205629707, 4.491214461102611,
     15.750030887441648, 12.117202397047082, 4.9661567773991635, 8.943235615043394, 6.0050450213744, 4.916783364708244,
     5.03461804799711, 1.5383549877288005, 6.107323716685965, 2.895592428682539, 7.093871228634743, 9.605283791104299,
     4.812559542235935, 3.1896185024560895, 2.623341190839591, 5.759718985431865, 9.409693586518904, 4.242547521967523,
     7.5372525906611045, 1.351035236596838, 14.335440253366743, 5.8354604145403925, 6.796890203622526,
     4.690104954194579, 6.020718233783919, 6.2094835793956875, 2.44038610287054, 10.469210548608766, 5.561673161627988,
     4.420172265566384, 9.599667237753255, 6.802965977889511, 4.627745618254304, 4.208894112628968, 3.495221926017363,
     2.649022505004613, 14.139495359076655, 2.6154906839741088, 7.091821305835752, 3.8317239814549806,
     8.118523797612678, 6.378341987976609, 4.942606031929391, 2.455666721016615, 3.766754985418921, 13.100882936342856,
     3.7120489827512544, 5.360056108870518, 1.1570575839646677, 4.689888912136206, 3.918394385033335,
     2.6726279515960814, 10.318664533127635, 7.496354988652445, 2.8989033224613205, 3.6120340912277653,
     3.0735892468462644, 0.8680733430154994, 9.28219359802861, 14.18880580325407, 4.528617211000682, 2.6191997754023983,
     11.380291755287839, 4.670148811743641, 13.314858856730424, 12.28062497763269, 4.961491977867267, 3.723855407905259,
     10.798305411261474, 4.767222704284638, 1.301215023163492, 10.061933051823903, 6.739013791142736,
     4.6078417724249245, 9.849190328310636, 4.744005231106855, 2.0908784208607365, 4.251157942738258, 3.09668357590831,
     6.2511155797705, 9.349969445437345, 21.883449148113357, 6.33053695373594, 7.056905743843439, 14.164769400954558,
     5.2951087370419, 5.897215140633886, 5.160445035879095, 4.700689341272399, 2.1951801093638106, 3.8031597889285504,
     10.151190209514803, 11.015226074981783, 3.310157490899494, 5.62604882537047, 2.195295430377642, 5.104272749341748,
     3.222486666010044, 5.174590009710277, 5.719632921533098, 6.268422325382671, 4.161382125850426, 4.367802758133617,
     4.68328412039309, 5.254309381072577, 8.98526633217417, 1.1437931859170556, 6.727222271321203, 3.3230915004872443,
     7.6905987750053075, 5.179385360605515, 3.0194713070338164, 5.393706390557604, 5.7804255188091185,
     4.288096116235953, 5.1023169459157485, 4.192524080575408, 5.424369920620723, 7.38991097423818, 3.4762430395818247,
     10.817766522615187, 13.287491059413139, 9.216966840312118, 10.19578229577946, 11.377174441428425,
     4.752129572528767, 3.5595677054921335, 5.978470021090466, 7.301163533959304, 4.045862093959009, 1.8943983748752702,
     8.88109044628139, 5.389201235403502, 6.219467877408058, 3.0839338242471124, 4.951339589725277, 4.6226877065690575,
     2.672712918743146, 6.887800042025458, 2.737998413987766, 1.530677815268982, 3.1039238820101387, 9.403502279795608,
     4.628778510758011, 7.537773703424617, 4.094250380243201, 6.959764226532933, 8.338949810956478, 8.684955859688761,
     8.805847214552951, 4.684533065284976, 18.227678902668657, 9.251750593572583, 2.1971271913845856,
     4.0424082409855195, 9.967835386046632, 8.568226170802962, 5.786264097231552, 7.227883554990648, 12.111123057257908,
     3.0282221373161544, 2.896202346908906, 5.99545197077493, 2.7705321846251705, 7.229456115505308, 10.735763898050035,
     16.880162513602656, 4.566419197155616, 11.51997835286082, 6.942479857589583, 9.37618733356939, 2.032026951162522,
     6.056115295089463, 7.236718075513413, 3.820009806382123, 4.621890782146837, 6.567814897746658, 9.16699107081574,
     3.8345179785691146, 5.433242777338487, 3.3620322608527915, 6.886438043329215, 7.454922351475799,
     14.806167920297401, 1.172164467258667, 8.505018317564875, 3.072677093440275, 10.644744275019846,
     6.4334741368992905, 6.513712067271362, 6.400959556887166, 4.076904131621876, 5.142816249789128, 8.140517849507102,
     4.470136410298877, 12.191775924866343, 7.547047160874115, 7.505925154875539, 7.721828011293502, 4.010371813032875,
     4.725962610089591, 3.657442996421701, 5.160461232308945, 8.94044140083862, 16.4448497409053, 1.679820056129746,
     2.5035856142520783, 2.1174388152893755, 9.769805159778716, 11.963386205297752, 4.142877443810893, 5.44615984800302,
     10.36091468001975, 5.2592691834511225, 7.431768829791105, 6.627166618238542, 6.584273154086006, 5.4140467838501865,
     2.9437652781713894, 3.236960054373994, 1.7249589010126214, 1.041979934810001, 11.154692540875219,
     10.365734511621485, 4.52149700478042, 11.852879566220622, 12.470042404751675, 3.027737105912011,
     1.5145710796492713, 3.4182787219740853, 10.013102897613177, 4.843069924770116, 4.69209439257933, 6.155425144352844,
     4.858445694988502, 6.212857401460237, 11.880885015188307, 7.138290216491488, 7.145306572313801, 7.730971453302077,
     11.75193049024426, 1.816066852778704, 6.444784996124673, 6.3918763983700835, 6.071368455159864, 5.900967864667777,
     6.931352803060733, 4.7290171964353265, 10.828734899129213, 5.3274699066761375, 4.879572481897503,
     2.226532834722847, 7.127320161226704, 2.133223431964671, 2.711014607887549, 5.167041214608078, 2.2529198655071534,
     3.2293493444077184, 4.232500053324749, 5.931377204769267, 6.353477603911372, 3.9957559976509245,
     13.419488137662762, 2.715021074274255, 5.920130249820991, 5.880245987130351, 8.039870654143748, 6.507585444575974,
     3.262033087203413, 5.921118717652465, 8.2940834564149, 4.649920341019877, 5.739030022717196, 3.190566384226668,
     0.5273863224468243, 10.637399132569165, 7.475189835808635, 12.099489653221392, 7.490938613698014,
     4.809600149644246, 1.9034262174621763, 5.526691206102858, 16.813776007910747, 10.607486934586348,
     7.6185837743501725, 3.50902128798446, 2.7042978339068675, 4.66927635414921, 7.92708432611199, 0.9245072808613892,
     0.707921177153447, 2.0587983054019854, 7.806073580779934, 1.8740240371395704, 1.2292411548358575,
     5.8069101284618885, 0.7949700012851761, 3.5967364590822717, 8.519960314381724, 1.001413432394441,
     1.7608942456882206, 2.8513086778287478, 13.136525314053417, 5.62232092393731, 1.6715745940811715, 9.05253837847488,
     8.800410737660613, 5.332435497148447, 3.3698112934715017, 11.403615213538128, 4.213458898519149, 4.913912721920302,
     2.6890842310625964, 1.1471493731419118, 3.5349822944315683, 3.8364924665765483, 3.254136410400278,
     6.12986717299446, 9.406747378178485, 3.2114216289103776, 6.881501055031677, 10.406054247151754, 5.460072492156269,
     5.2972779858045795, 6.75916725919274, 9.164409529964127, 4.2520747378570105, 7.72736604883265, 7.600085268406471,
     5.088611238230976, 0.7658211710525957, 0.6952312129409309, 8.541086427381277, 8.587997912167362,
     11.600378916455933, 5.792495955321485, 1.3975234002166088, 0.5610480057395055, 5.462522644498766,
     3.2273242283124324, 6.136363387882641, 1.0689882660311536, 0.7482795275267435, 3.727975463605759, 5.35343201951353,
     17.620003333458975, 8.988860361373618, 10.897097701293003, 3.3684112315603727, 5.699096054002369,
     2.2098412062297275, 4.88553949017383, 9.248104641952363, 4.70041069692071, 0.8401332070250564, 8.807985312441108,
     2.462202744969694, 7.393370577401274, 15.292585950931194, 2.393456381646037, 2.169551073430023, 5.783326426188347,
     5.672754291744656, 3.9125826156602224, 3.9261898787743394, 2.878470378811758, 4.951395940700337, 7.4087744717391,
     5.928870709888734, 5.1720628010708225, 2.632979146585198, 5.97775624716972, 5.45363563410371, 6.343745928938196,
     8.64058599592793, 6.913752601297968, 5.028752973789009, 6.043709080369069, 13.063254636006995, 15.970204790635046,
     5.877597872905224, 5.172831296687192, 2.1855094181307817, 4.031944209022251, 2.785842207878688, 3.502414645337115,
     6.405535607956378, 6.29553879263592, 4.59153185297753, 11.269280202509336, 4.260697888712722, 5.309942402649254,
     2.330654977674441, 4.344143177741036, 6.650923394014688, 4.365674257283331, 2.080322696347704, 3.8150074726546124,
     5.855728483570144, 5.20431671687842, 5.247185283972854, 5.737102736175476, 3.9045579611405636, 3.2915449565070336,
     4.785497796658335, 14.743047929057763, 5.229262260677498, 5.127892732516028, 11.629502748310099, 5.38195038617398,
     4.471226713414872, 11.413520380063204, 6.115423149210802, 4.671228212675052, 3.2597617894460567, 4.292277628207318,
     3.0288289114841, 23.44899552775188, 6.943285344103334, 1.6621617980289634, 4.6345241129066705, 12.266143583493026,
     9.479989087118621, 8.624728398417815, 4.883535841766543, 2.0127236721332853, 6.339682672965372, 3.1671537237484406,
     3.2687449466075997, 6.0951966533755995, 4.384720395848596, 4.399012880119121, 6.006761669275152, 4.748677737679622,
     5.617100933463576, 1.0743595263755041, 5.230184776058039, 4.234402726354673, 7.820109243395914, 2.9321327001083732,
     2.6332315237665265, 4.73568385043203, 4.975151243058565, 3.1728492606288645, 7.017806434712625, 2.460259802500177,
     3.0547072524722894, 4.812245453841134, 2.624613917988751, 6.6702539269102346, 8.590050301048722, 9.791293752759113,
     7.122171084338005, 9.671082891097257, 3.9208522190151247, 6.290606881352096, 3.213583586489973, 17.96664723134716,
     5.873026928065197, 2.6857603514361763, 10.257551087887638, 11.724556615773396, 4.672809978514584,
     3.796079732282383, 1.2864722219447131, 3.0279987727091506, 7.9773753582350055, 5.351847645700804,
     5.518907585933399, 3.4273716171695963, 6.277782087395575, 3.727413191264625, 13.165535551259808, 7.554181734957412,
     1.6973749334255592, 7.470408017204967, 9.357725456039445, 1.409963227943507, 7.952240694686496, 6.974985380056287,
     6.295465451757811, 3.8897543408385333, 4.211690972233504, 2.1571256336565208, 1.5931685664538382,
     6.662476039686312, 6.9204786083825995, 2.980891683294911, 3.9973411839980426, 5.41706449307553, 14.028526336033313,
     8.868911436376901, 4.680001074976787, 13.111435380156674, 14.270161953212707, 1.1819509578631395,
     4.7863413204025385, 4.15319622915864, 5.470567445757288, 4.220326300612822, 5.586037192063384, 2.5252977318938576,
     4.775656054865033, 0.9237883440600135, 12.828262875227837, 4.885895913481079, 6.120726467015681, 2.939758335936759,
     5.317228200522224, 5.978646401616096, 4.273749738637804, 9.366335632528685, 2.5967324117178934, 8.45235451639357,
     6.735771263996401, 4.961412937710448, 4.072529944099302, 10.916366299869754, 3.6111021415050475, 5.72675460014605,
     12.526262487067985, 7.700426179912183, 2.0921099377245453, 6.14830797928356, 4.643647996210977, 6.570372756578376,
     5.340846033809671, 22.697757095035477, 7.04088580194939, 0.557143515097851, 5.154950566933169, 0.4661521298061278,
     0.4975731525893352, 8.131657191161201, 2.0010263846781697, 4.929338313200194, 5.443468222654193, 5.167093691323087,
     6.947289276618228, 4.256798417677625, 10.625366251588915, 9.703417583707868, 3.921067287241002, 2.6228711301809415,
     9.96113453476045, 4.250738018873776, 3.2535158618645945, 3.1116807401345126, 8.36454447216764, 7.115817289346733,
     3.4091341927106757, 2.5095395104886977, 3.8832730348524973, 7.841807019290483, 4.1670656638911385, 7.0208004597501,
     4.82319500988684, 7.326414582287808, 8.087756804803863, 4.097607890462156, 6.597520935745374, 14.082860995558189,
     3.2247478398285754, 9.066873973330493, 8.804911745474412, 9.022041408903542, 5.634403138188716, 10.868902242129964,
     9.839238015951887, 7.167869862733031, 6.6283765126417515, 6.8853374434527925, 10.635219983288854,
     4.646178861573052, 6.200458037144456, 9.231268790198826, 6.675619751839706, 10.57984110464204, 8.640740503588901,
     4.1861739665820865, 5.180298113684646, 5.985525332639949, 0.715486049278027, 4.510748456727681, 8.89201018523459,
     0.45599492111984585, 2.4006064998086165, 2.245278655139749, 10.05967345691578, 9.732056436658446,
     10.060947943174636, 4.399767861766289, 8.13754202322081, 8.133208942743753, 3.7585698675998005, 1.539849618223503,
     4.458024278583307, 6.239801535629567, 2.204844608647999, 4.581994980461454, 2.8849091654906998, 4.8161681498438575,
     2.5527220490728775, 3.482080964554934, 6.8895095621243705, 3.152549889097246, 3.657606289264871,
     1.8869753859047995, 5.322655674603405, 3.4058293282009107, 13.389237186453808, 7.312071647761987,
     12.763556599404318, 4.167265845367611, 6.576918224236572, 6.799522300601156, 2.990305713240023, 2.357679121155081,
     3.310235884205309, 6.535938870192582, 1.3297463703095844, 2.4168943404822674, 6.143049018798267, 2.201168021088345,
     1.8965146251427032, 5.637101760718702, 2.7046712363941365, 6.449198707700952, 3.2513271685460823,
     6.3200806253426975, 5.600039719568073, 0.991990877442601, 3.616964486708931, 4.897649433273062, 1.6708272244474935,
     7.355044927548512, 6.47374686266931, 6.805327155288172, 8.282642415804306, 9.172094478252358, 2.2178158135143247,
     14.322187506814467, 7.977793628027315, 3.8542697209527264, 6.217117276560632, 11.500067781806296,
     6.225986125612551, 6.387637004999169, 2.9030953822806262, 10.697647316646545, 9.346042428653012, 3.86117316495083,
     0.8774041689295353, 4.909752915478119, 7.473067193444233, 10.389469193868802, 5.709766160389223, 8.468052694976587,
     4.2643663558528875, 13.987436344356077, 8.179427711473366, 1.8038015007740702, 4.916146100236836,
     4.690990615186386, 4.761677781054899, 6.459982419525412, 5.780296902131995, 2.762518795035417, 5.1079821094687645,
     4.352928341836902, 7.405109122492712, 4.764834535819109, 3.3675643120762135, 5.4241567661759955,
     1.9910727518799334, 13.368684833853287, 3.070784609587685, 7.14302179015546, 2.3154727549308447,
     14.903738807988955, 5.476647632855194, 7.972453231141758, 4.832794352056428, 13.38100692278653, 4.650428255440264,
     4.8953420244627335, 5.516234788098224, 8.075116089133878, 4.001646472816837, 16.824124091892944,
     10.024882031571101, 7.500444752535754, 5.722877531799959, 3.9633058352265023, 3.648871456063504,
     3.1125531200913485, 4.312860991448464, 7.879881301123978, 3.337175211255941, 4.937943948975762, 1.269269245255193,
     8.026770620024504, 2.3954297253625185, 13.121652674313939, 4.988956251361257, 5.82074598765103, 8.644512522688391,
     8.165257739126305, 3.0038403503550244, 3.479461979119327, 10.178960150720318, 6.793408112093986, 8.268752455487293,
     10.94129744947698, 7.717107133836036, 2.301678382005478, 3.0836112991762503, 6.413363714731343, 12.337981743552898,
     5.290653346673792, 6.161205505382587, 4.337069937528138, 12.595665832978968, 7.9113421371699495, 4.230648808499726,
     5.41318349484286, 3.2150141678950854, 1.8488048713934195, 6.596617597715968, 4.59815669040584, 20.95610829997896,
     9.91273957082278, 5.18216124193026, 5.0855048577780995, 6.752576297991004, 6.53996100109581, 2.11714855564943,
     5.588972322478199, 9.013522798625935, 5.756524654142731, 7.853786177879321, 11.513712912087806, 5.782292941038641,
     4.865358590248189, 4.942504681224539, 6.382662779161127, 2.726063442863018, 1.446789677291923, 2.670493803094094,
     2.6375071456363193, 15.345443557337918, 2.8657754896019547, 7.018987752686018, 8.761685083358167,
     5.481249263152243, 12.549990274760994, 2.60604806824855, 6.941499689792451, 5.645905905439542, 13.524008388253336,
     2.8192420514248786, 6.359034278489952, 5.027957131470407, 7.547154475183, 11.089914423674452, 11.103331313587208,
     9.101856106780183, 2.127318568133937, 3.2379181272922457, 5.440631438007583, 14.909503567626874, 5.884030800904881,
     8.587272302575663, 2.3508848216114426, 7.380667342116574, 4.537533553714365, 6.793591927864465, 6.218986082491446,
     4.0215736769332295]

    params = ss.gamma.fit(gD_3_2)

    print("P: {}".format(params))

    params = ss.gamma.fit(gD_3_2, floc=0.0)

    print("P: {}".format(params))
    assert abs(params[0] - 3) < 0.05