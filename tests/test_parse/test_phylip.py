#!/bin/env python
#file cogent/parse/test_phylip.py
"""Unit tests for the phylip parser
"""
from cogent.parse.phylip import MinimalPhylipParser, get_align_for_phylip
from cogent.parse.record import RecordError
from cogent.util.unit_test import TestCase, main
from StringIO import StringIO

__author__ = "Micah Hamady"
__copyright__ = "Copyright 2007-2011, The Cogent Project"
__credits__ = ["Micah Hamady", "Rob Knight"]
__license__ = "GPL"
__version__ = "1.6.0.dev"
__maintainer__ = "Micah Hamady"
__email__ = "hamady@colorado.edu"
__status__ = "Production"

class PhylipGenericTest(TestCase):
    """Setup data for Phylip parsers."""
    def setUp(self):
        """standard files"""
        self.big_interleaved = StringIO("""10 705 I
Cow       ATGGCATATCCCATACAACTAGGATTCCAAGATGCAACATCACCAATCATAGAAGAACTA
Carp      ATGGCACACCCAACGCAACTAGGTTTCAAGGACGCGGCCATACCCGTTATAGAGGAACTT
Chicken   ATGGCCAACCACTCCCAACTAGGCTTTCAAGACGCCTCATCCCCCATCATAGAAGAGCTC
Human     ATGGCACATGCAGCGCAAGTAGGTCTACAAGACGCTACTTCCCCTATCATAGAAGAGCTT
Loach     ATGGCACATCCCACACAATTAGGATTCCAAGACGCGGCCTCACCCGTAATAGAAGAACTT
Mouse     ATGGCCTACCCATTCCAACTTGGTCTACAAGACGCCACATCCCCTATTATAGAAGAGCTA
Rat       ATGGCTTACCCATTTCAACTTGGCTTACAAGACGCTACATCACCTATCATAGAAGAACTT
Seal      ATGGCATACCCCCTACAAATAGGCCTACAAGATGCAACCTCTCCCATTATAGAGGAGTTA
Whale     ATGGCATATCCATTCCAACTAGGTTTCCAAGATGCAGCATCACCCATCATAGAAGAGCTC
Frog      ATGGCACACCCATCACAATTAGGTTTTCAAGACGCAGCCTCTCCAATTATAGAAGAATTA

CTTCACTTTCATGACCACACGCTAATAATTGTCTTCTTAATTAGCTCATTAGTACTTTAC
CTTCACTTCCACGACCACGCATTAATAATTGTGCTCCTAATTAGCACTTTAGTTTTATAT
GTTGAATTCCACGACCACGCCCTGATAGTCGCACTAGCAATTTGCAGCTTAGTACTCTAC
ATCACCTTTCATGATCACGCCCTCATAATCATTTTCCTTATCTGCTTCCTAGTCCTGTAT
CTTCACTTCCATGACCATGCCCTAATAATTGTATTTTTGATTAGCGCCCTAGTACTTTAT
ATAAATTTCCATGATCACACACTAATAATTGTTTTCCTAATTAGCTCCTTAGTCCTCTAT
ACAAACTTTCATGACCACACCCTAATAATTGTATTCCTCATCAGCTCCCTAGTACTTTAT
CTACACTTCCATGACCACACATTAATAATTGTGTTCCTAATTAGCTCATTAGTACTCTAC
CTACACTTTCACGATCATACACTAATAATCGTTTTTCTAATTAGCTCTTTAGTTCTCTAC
CTTCACTTCCACGACCATACCCTCATAGCCGTTTTTCTTATTAGTACGCTAGTTCTTTAC

ATTATTTCACTAATACTAACGACAAAGCTGACCCATACAAGCACGATAGATGCACAAGAA
ATTATTACTGCAATGGTATCAACTAAACTTACTAATAAATATATTCTAGACTCCCAAGAA
CTTCTAACTCTTATACTTATAGAAAAACTATCA---TCAAACACCGTAGATGCCCAAGAA
GCCCTTTTCCTAACACTCACAACAAAACTAACTAATACTAACATCTCAGACGCTCAGGAA
GTTATTATTACAACCGTCTCAACAAAACTCACTAACATATATATTTTGGACTCACAAGAA
ATCATCTCGCTAATATTAACAACAAAACTAACACATACAAGCACAATAGATGCACAAGAA
ATTATTTCACTAATACTAACAACAAAACTAACACACACAAGCACAATAGACGCCCAAGAA
ATTATCTCACTTATACTAACCACGAAACTCACCCACACAAGTACAATAGACGCACAAGAA
ATTATTACCCTAATGCTTACAACCAAATTAACACATACTAGTACAATAGACGCCCAAGAA
ATTATTACTATTATAATAACTACTAAACTAACTAATACAAACCTAATGGACGCACAAGAG

GTAGAGACAATCTGAACCATTCTGCCCGCCATCATCTTAATTCTAATTGCTCTTCCTTCT
ATCGAAATCGTATGAACCATTCTACCAGCCGTCATTTTAGTACTAATCGCCCTGCCCTCC
GTTGAACTAATCTGAACCATCCTACCCGCTATTGTCCTAGTCCTGCTTGCCCTCCCCTCC
ATAGAAACCGTCTGAACTATCCTGCCCGCCATCATCCTAGTCCTCATCGCCCTCCCATCC
ATTGAAATCGTATGAACTGTGCTCCCTGCCCTAATCCTCATTTTAATCGCCCTCCCCTCA
GTTGAAACCATTTGAACTATTCTACCAGCTGTAATCCTTATCATAATTGCTCTCCCCTCT
GTAGAAACAATTTGAACAATTCTCCCAGCTGTCATTCTTATTCTAATTGCCCTTCCCTCC
GTGGAAACGGTGTGAACGATCCTACCCGCTATCATTTTAATTCTCATTGCCCTACCATCA
GTAGAAACTGTCTGAACTATCCTCCCAGCCATTATCTTAATTTTAATTGCCTTGCCTTCA
ATCGAAATAGTGTGAACTATTATACCAGCTATTAGCCTCATCATAATTGCCCTTCCATCC

TTACGAATTCTATACATAATAGATGAAATCAATAACCCATCTCTTACAGTAAAAACCATA
CTACGCATCCTGTACCTTATAGACGAAATTAACGACCCTCACCTGACAATTAAAGCAATA
CTCCAAATCCTCTACATAATAGACGAAATCGACGAACCTGATCTCACCCTAAAAGCCATC
CTACGCATCCTTTACATAACAGACGAGGTCAACGATCCCTCCCTTACCATCAAATCAATT
CTACGAATTCTATATCTTATAGACGAGATTAATGACCCCCACCTAACAATTAAGGCCATG
CTACGCATTCTATATATAATAGACGAAATCAACAACCCCGTATTAACCGTTAAAACCATA
CTACGAATTCTATACATAATAGACGAGATTAATAACCCAGTTCTAACAGTAAAAACTATA
TTACGAATCCTCTACATAATGGACGAGATCAATAACCCTTCCTTGACCGTAAAAACTATA
TTACGGATCCTTTACATAATAGACGAAGTCAATAACCCCTCCCTCACTGTAAAAACAATA
CTTCGTATCCTATATTTAATAGATGAAGTTAATGATCCACACTTAACAATTAAAGCAATC

GGACATCAGTGATACTGAAGCTATGAGTATACAGATTATGAGGACTTAAGCTTCGACTCC
GGACACCAATGATACTGAAGTTACGAGTATACAGACTATGAAAATCTAGGATTCGACTCC
GGACACCAATGATACTGAACCTATGAATACACAGACTTCAAGGACCTCTCATTTGACTCC
GGCCACCAATGGTACTGAACCTACGAGTACACCGACTACGGCGGACTAATCTTCAACTCC
GGGCACCAATGATACTGAAGCTACGAGTATACTGATTATGAAAACTTAAGTTTTGACTCC
GGGCACCAATGATACTGAAGCTACGAATATACTGACTATGAAGACCTATGCTTTGATTCA
GGACACCAATGATACTGAAGCTATGAATATACTGACTATGAAGACCTATGCTTTGACTCC
GGACATCAGTGATACTGAAGCTATGAGTACACAGACTACGAAGACCTGAACTTTGACTCA
GGTCACCAATGATATTGAAGCTATGAGTATACCGACTACGAAGACCTAAGCTTCGACTCC
GGCCACCAATGATACTGAAGCTACGAATATACTAACTATGAGGATCTCTCATTTGACTCT

TACATAATTCCAACATCAGAATTAAAGCCAGGGGAGCTACGACTATTAGAAGTCGATAAT
TATATAGTACCAACCCAAGACCTTGCCCCCGGACAATTCCGACTTCTGGAAACAGACCAC
TACATAACCCCAACAACAGACCTCCCCCTAGGCCACTTCCGCCTACTAGAAGTCGACCAT
TACATACTTCCCCCATTATTCCTAGAACCAGGCGACCTGCGACTCCTTGACGTTGACAAT
TACATAATCCCCACCCAGGACCTAACCCCTGGACAATTCCGGCTACTAGAGACAGACCAC
TATATAATCCCAACAAACGACCTAAAACCTGGTGAACTACGACTGCTAGAAGTTGATAAC
TACATAATCCCAACCAATGACCTAAAACCAGGTGAACTTCGTCTATTAGAAGTTGATAAT
TATATGATCCCCACACAAGAACTAAAGCCCGGAGAACTACGACTGCTAGAAGTAGACAAT
TATATAATCCCAACATCAGACCTAAAGCCAGGAGAACTACGATTATTAGAAGTAGATAAC
TATATAATTCCAACTAATGACCTTACCCCTGGACAATTCCGGCTGCTAGAAGTTGATAAT

CGAGTTGTACTACCAATAGAAATAACAATCCGAATGTTAGTCTCCTCTGAAGACGTATTA
CGAATAGTTGTTCCAATAGAATCCCCAGTCCGTGTCCTAGTATCTGCTGAAGACGTGCTA
CGCATTGTAATCCCCATAGAATCCCCCATTCGAGTAATCATCACCGCTGATGACGTCCTC
CGAGTAGTACTCCCGATTGAAGCCCCCATTCGTATAATAATTACATCACAAGACGTCTTG
CGAATGGTTGTTCCCATAGAATCCCCTATTCGCATTCTTGTTTCCGCCGAAGATGTACTA
CGAGTCGTTCTGCCAATAGAACTTCCAATCCGTATATTAATTTCATCTGAAGACGTCCTC
CGGGTAGTCTTACCAATAGAACTTCCAATTCGTATACTAATCTCATCCGAAGACGTCCTG
CGAGTAGTCCTCCCAATAGAAATAACAATCCGCATACTAATCTCATCAGAAGATGTACTC
CGAGTTGTCTTACCTATAGAAATAACAATCCGAATATTAGTCTCATCAGAAGACGTACTC
CGAATAGTAGTCCCAATAGAATCTCCAACCCGACTTTTAGTTACAGCCGAAGACGTCCTC

CACTCATGAGCTGTGCCCTCTCTAGGACTAAAAACAGACGCAATCCCAGGCCGTCTAAAC
CATTCTTGAGCTGTTCCATCCCTTGGCGTAAAAATGGACGCAGTCCCAGGACGACTAAAT
CACTCATGAGCCGTACCCGCCCTCGGGGTAAAAACAGACGCAATCCCTGGACGACTAAAT
CACTCATGAGCTGTCCCCACATTAGGCTTAAAAACAGATGCAATTCCCGGACGTCTAAAC
CACTCCTGGGCCCTTCCAGCCATGGGGGTAAAGATAGACGCGGTCCCAGGACGCCTTAAC
CACTCATGAGCAGTCCCCTCCCTAGGACTTAAAACTGATGCCATCCCAGGCCGACTAAAT
CACTCATGAGCCATCCCTTCACTAGGGTTAAAAACCGACGCAATCCCCGGCCGCCTAAAC
CACTCATGAGCCGTACCGTCCCTAGGACTAAAAACTGATGCTATCCCAGGACGACTAAAC
CACTCATGGGCCGTACCCTCCTTGGGCCTAAAAACAGATGCAATCCCAGGACGCCTAAAC
CACTCGTGAGCTGTACCCTCCTTGGGTGTCAAAACAGATGCAATCCCAGGACGACTTCAT

CAAACAACCCTTATATCGTCCCGTCCAGGCTTATATTACGGTCAATGCTCAGAAATTTGC
CAAGCCGCCTTTATTGCCTCACGCCCAGGGGTCTTTTACGGACAATGCTCTGAAATTTGT
CAAACCTCCTTCATCACCACTCGACCAGGAGTGTTTTACGGACAATGCTCAGAAATCTGC
CAAACCACTTTCACCGCTACACGACCGGGGGTATACTACGGTCAATGCTCTGAAATCTGT
CAAACCGCCTTTATTGCCTCCCGCCCCGGGGTATTCTATGGGCAATGCTCAGAAATCTGT
CAAGCAACAGTAACATCAAACCGACCAGGGTTATTCTATGGCCAATGCTCTGAAATTTGT
CAAGCTACAGTCACATCAAACCGACCAGGTCTATTCTATGGCCAATGCTCTGAAATTTGC
CAAACAACCCTAATAACCATACGACCAGGACTGTACTACGGTCAATGCTCAGAAATCTGT
CAAACAACCTTAATATCAACACGACCAGGCCTATTTTATGGACAATGCTCAGAGATCTGC
CAAACATCATTTATTGCTACTCGTCCGGGAGTATTTTACGGACAATGTTCAGAAATTTGC

GGGTCAAACCACAGTTTCATACCCATTGTCCTTGAGTTAGTCCCACTAAAGTACTTTGAA
GGAGCTAATCACAGCTTTATACCAATTGTAGTTGAAGCAGTACCTCTCGAACACTTCGAA
GGAGCTAACCACAGCTACATACCCATTGTAGTAGAGTCTACCCCCCTAAAACACTTTGAA
GGAGCAAACCACAGTTTCATGCCCATCGTCCTAGAATTAATTCCCCTAAAAATCTTTGAA
GGAGCAAACCACAGCTTTATACCCATCGTAGTAGAAGCGGTCCCACTATCTCACTTCGAA
GGATCTAACCATAGCTTTATGCCCATTGTCCTAGAAATGGTTCCACTAAAATATTTCGAA
GGCTCAAATCACAGCTTCATACCCATTGTACTAGAAATAGTGCCTCTAAAATATTTCGAA
GGTTCAAACCACAGCTTCATACCTATTGTCCTCGAATTGGTCCCACTATCCCACTTCGAG
GGCTCAAACCACAGTTTCATACCAATTGTCCTAGAACTAGTACCCCTAGAAGTCTTTGAA
GGAGCAAACCACAGCTTTATACCAATTGTAGTTGAAGCAGTACCGCTAACCGACTTTGAA

AAATGATCTGCGTCAATATTA---------------------TAA
AACTGATCCTCATTAATACTAGAAGACGCCTCGCTAGGAAGCTAA
GCCTGATCCTCACTA------------------CTGTCATCTTAA
ATA---------------------GGGCCCGTATTTACCCTATAG
AACTGGTCCACCCTTATACTAAAAGACGCCTCACTAGGAAGCTAA
AACTGATCTGCTTCAATAATT---------------------TAA
AACTGATCAGCTTCTATAATT---------------------TAA
AAATGATCTACCTCAATGCTT---------------------TAA
AAATGATCTGTATCAATACTA---------------------TAA
AACTGATCTTCATCAATACTA---GAAGCATCACTA------AGA
        """)

        self.space_interleaved = StringIO(""" 5 176 I
cox2_leita   MAFILSFWMI FLLDSVIVLL SFVCFVCVWI CALLFSTVLL VSKLNNIYCT
cox2_crifa   MAFILSFWMI FLIDAVIVLL SFVCFVCIWI CSLFFSSFLL VSKINNVYCT
cox2_bsalt   MSFIISFWML FLIDSLIVLL SGAIFVCIWI CSLFFLCILF ICKLDYIFCS
cox2_trybb   MSFILTFWMI FLMDSIIVLI SFSIFLSVWI CALIIATVLT VTKINNIYCT
cox2_tborr   MLFFINQLLL LLVDTFVILE IFSLFVCVFI IVMYILFINY NIFLKNINVY

             WDFTASKFID VYWFTIGGMF SLGLLLRLCL LLYFGHLNFV SFDLCKVVGF
             WDFTASKFID AYWFTIGGMF VLCLLLRLCL LLYFGCLNFV SFDLCKVVGF
             WDFISAKFID LYWFTLGCLF IVCLLIRLCL LLYFSCLNFV CFDLCKCIGF
             WDFISSKFID TYWFVLGMMF ILCLLLRLCL LLYFSCINFV SFDLCKVIGF
             LDFIGSKYLD LYWFLIGIFF VIVLLIRLCL LLYYSWISLL IFDLCKIMGF
             
             QWYWVYFIFG ETTIFSNLIL ESDYMIGDLR LLQCNHVLTL LSLVIYKLWL
             QWYWVYFIFG ETTIFSNLIL ESDYLIGDLR LLQCNHVLTL LSLVIYKLWL
             QWYWVYFIFG ETTIFSNLIL ESDYLIGDLR LLQCNHVLTL LSLVIYKVWL
             QWYWVYFLFG ETTIFSNLIL ESDYLIGDLR ILQCNHVLTL LSLVIYKLWV
             QWYWIFFVFK ENVIFSNLLI ESDYWIGDLR LLQCNNTFNL ICLVVYKIWV
             
             SAVDVIHSFA ISSLGVKVEN LVAVMK
             SAVDVIHSFA VSSLGIKVDC IPGRCN
             SAIDVIHSFT LANLGIKVD? ?PGRCN
             SAVDVIHSFT ISSLGIKVEN PGRCNE
             TSIDVIHSFT ISTLGIKIDC IPGRCN
                                                                                                                                                                """)
        self.interleaved_little = StringIO("""   6   39 I
Archaeopt CGATGCTTAC CGCCGATGCT
HesperorniCGTTACTCGT TGTCGTTACT
BaluchitheTAATGTTAAT TGTTAATGTT
B. virginiTAATGTTCGT TGTTAATGTT
BrontosaurCAAAACCCAT CATCAAAACC
B.subtilisGGCAGCCAAT CACGGCAGCC

TACCGCCGAT GCTTACCGC
CGTTGTCGTT ACTCGTTGT
AATTGTTAAT GTTAATTGT
CGTTGTTAAT GTTCGTTGT
CATCATCAAA ACCCATCAT
AATCACGGCA GCCAATCAC
""")
        self.empty = []

        self.noninterleaved_little = StringIO("""   6   20

Archaeopt CGATGCTTAC CGCCGATGCT
HesperorniCGTTACTCGT TGTCGTTACT

BaluchitheTAATGTTAAT TGTTAATGTT
B. virginiTAATGTTCGT TGTTAATGTT
BrontosaurCAAAACCCAT CATCAAAACC
B.subtilisGGCAGCCAAT CACGGCAGCC

""")

        self.noninterleaved_big = StringIO("""10  297
Rhesus    tgtggcacaaatactcatgccagctcattacagcatgagaac---agtttgttactcact
          aaagacagaatgaatgtagaaaaggctgaattctgtaataaaagcaaacagcctggcttg
          gcaaggagccaacataacagatggactggaagtaaggaaacatgtaatgataggcagact
          cccagcacagagaaaaaggtagatctgaatgctaatgccctgtatgagagaaaagaatgg
          aataagcaaaaactgccatgctctgagaatcctagagacactgaagatgttccttgg
Manatee   tgtggcacaaatactcatgccagctcattacagcatgagaatagcagtttattactcact
          aaagacagaatgaatgtagaaaaggctgaattctgtcataaaagcaaacagcctggctta
          acaaggagccagcagagcagatgggctgaaagtaaggaaacatgtaatgataggcagact
          cctagcacagagaaaaaggtagatatgaatgctaatccattgtatgagagaaaagaagtg
          aataagcagaaacctccatgctccgagagtgttagagatacacaagatattccttgg
Pig       tgtggcacagatactcatgccagctcgttacagcatgagaacagcagtttattactcact
          aaagacagaatgaatgtagaaaaggctgaattttgtaataaaagcaagcagcctgtctta
          gcaaagagccaacagagcagatgggctgaaagtaagggcacatgtaatgataggcagact
          cctaacacagagaaaaaggtagttctgaatactgatctcctgtatgggagaaacgaactg
          aataagcagaaacctgcgtgctctgacagtcctagagattcccaagatgttccttgg
""")
 
class MinimalPhylipParserTests(PhylipGenericTest):
    """Tests of MinimalPhylipParser: returns (label, seq) tuples."""
       
    def test_empty(self):
        """MinimalFastaParser should return empty list from 'file' w/o labels"""
        self.assertEqual(list(MinimalPhylipParser(self.empty)), [])

    def test_minimal_parser(self):
        """MinimalFastaParser should read single record as (label, seq) tuple"""
        seqs = list(MinimalPhylipParser(self.big_interleaved))
        self.assertEqual(len(seqs), 10)
        label, seq = seqs[-1]
        self.assertEqual(label, 'Frog')
        self.assertEqual(seq, \
'ATGGCACACCCATCACAATTAGGTTTTCAAGACGCAGCCTCTCCAATTATAGAAGAATTACTTCACTTCCACGACCATACCCTCATAGCCGTTTTTCTTATTAGTACGCTAGTTCTTTACATTATTACTATTATAATAACTACTAAACTAACTAATACAAACCTAATGGACGCACAAGAGATCGAAATAGTGTGAACTATTATACCAGCTATTAGCCTCATCATAATTGCCCTTCCATCCCTTCGTATCCTATATTTAATAGATGAAGTTAATGATCCACACTTAACAATTAAAGCAATCGGCCACCAATGATACTGAAGCTACGAATATACTAACTATGAGGATCTCTCATTTGACTCTTATATAATTCCAACTAATGACCTTACCCCTGGACAATTCCGGCTGCTAGAAGTTGATAATCGAATAGTAGTCCCAATAGAATCTCCAACCCGACTTTTAGTTACAGCCGAAGACGTCCTCCACTCGTGAGCTGTACCCTCCTTGGGTGTCAAAACAGATGCAATCCCAGGACGACTTCATCAAACATCATTTATTGCTACTCGTCCGGGAGTATTTTACGGACAATGTTCAGAAATTTGCGGAGCAAACCACAGCTTTATACCAATTGTAGTTGAAGCAGTACCGCTAACCGACTTTGAAAACTGATCTTCATCAATACTA---GAAGCATCACTA------AGA')
        self.assertEqual(seqs[0][0], 'Cow')

        seqs = list(MinimalPhylipParser(self.space_interleaved))
        self.assertEqual(len(seqs), 5)
        self.assertEqual(seqs[0][0], 'cox2_leita')
        self.assertEqual(seqs[-1][0], 'cox2_tborr')
        self.assertEqual(len(seqs[0][1]), 176)
        self.assertEqual(len(seqs[-1][1]), 176)

        seqs = list(MinimalPhylipParser(self.interleaved_little))
        self.assertEqual(len(seqs), 6)
        self.assertEqual(seqs[1][0], 'Hesperorni')
        self.assertEqual(seqs[-1][0], 'B.subtilis')
        self.assertEqual(seqs[-1][1], 'GGCAGCCAATCACGGCAGCCAATCACGGCAGCCAATCAC')

        seqs = list(MinimalPhylipParser(self.noninterleaved_little))
        self.assertEqual(len(seqs), 6)
        self.assertEqual(seqs[0][0], 'Archaeopt')
        self.assertEqual(seqs[-1][0], 'B.subtilis')
        self.assertEqual(seqs[-1][-1], 'GGCAGCCAATCACGGCAGCC')

        seqs = list(MinimalPhylipParser(self.noninterleaved_big))
        self.assertEqual(len(seqs), 3)
        self.assertEqual(seqs[0][0], 'Rhesus')
        self.assertEqual(seqs[-1][0], 'Pig')
        self.assertEqual(seqs[-1][1], 'tgtggcacagatactcatgccagctcgttacagcatgagaacagcagtttattactcactaaagacagaatgaatgtagaaaaggctgaattttgtaataaaagcaagcagcctgtcttagcaaagagccaacagagcagatgggctgaaagtaagggcacatgtaatgataggcagactcctaacacagagaaaaaggtagttctgaatactgatctcctgtatgggagaaacgaactgaataagcagaaacctgcgtgctctgacagtcctagagattcccaagatgttccttgg')

    def test_get_align(self):
        """get_align_for_phylip should return Aligment object for phylip files"""
        align = get_align_for_phylip(self.big_interleaved)
        align = get_align_for_phylip(self.interleaved_little)
        s = str(align)
        self.assertEqual(s, '''>Archaeopt
CGATGCTTACCGCCGATGCTTACCGCCGATGCTTACCGC
>Hesperorni
CGTTACTCGTTGTCGTTACTCGTTGTCGTTACTCGTTGT
>Baluchithe
TAATGTTAATTGTTAATGTTAATTGTTAATGTTAATTGT
>B. virgini
TAATGTTCGTTGTTAATGTTCGTTGTTAATGTTCGTTGT
>Brontosaur
CAAAACCCATCATCAAAACCCATCATCAAAACCCATCAT
>B.subtilis
GGCAGCCAATCACGGCAGCCAATCACGGCAGCCAATCAC
''')
        align = get_align_for_phylip(self.noninterleaved_little)
        s = str(align)
        self.assertEqual(s, '''>Archaeopt
CGATGCTTACCGCCGATGCT
>Hesperorni
CGTTACTCGTTGTCGTTACT
>Baluchithe
TAATGTTAATTGTTAATGTT
>B. virgini
TAATGTTCGTTGTTAATGTT
>Brontosaur
CAAAACCCATCATCAAAACC
>B.subtilis
GGCAGCCAATCACGGCAGCC
''')
             
if __name__ == '__main__':
    main()
