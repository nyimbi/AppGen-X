# Generated from lang/appgen.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,61,587,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,1,0,3,0,96,8,0,1,0,5,0,99,8,0,10,0,12,0,102,9,0,1,0,1,0,1,1,
        1,1,3,1,108,8,1,1,1,3,1,111,8,1,1,2,1,2,5,2,115,8,2,10,2,12,2,118,
        9,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,5,3,127,8,3,10,3,12,3,130,9,3,1,
        3,3,3,133,8,3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,4,1,4,1,4,3,4,152,8,4,1,5,1,5,1,5,1,5,1,6,1,6,5,6,160,8,
        6,10,6,12,6,163,9,6,1,6,1,6,1,7,1,7,1,7,3,7,170,8,7,1,8,1,8,1,8,
        1,8,3,8,176,8,8,1,8,5,8,179,8,8,10,8,12,8,182,9,8,1,8,3,8,185,8,
        8,1,9,1,9,1,9,3,9,190,8,9,1,10,1,10,1,10,1,11,1,11,1,11,1,12,1,12,
        1,12,1,12,3,12,202,8,12,1,12,1,12,3,12,206,8,12,1,13,1,13,1,13,1,
        13,1,13,1,13,1,13,1,13,1,13,1,13,3,13,218,8,13,1,13,1,13,1,13,3,
        13,223,8,13,3,13,225,8,13,1,14,3,14,228,8,14,1,14,1,14,1,14,1,14,
        3,14,234,8,14,1,14,3,14,237,8,14,1,15,1,15,1,15,1,15,1,16,1,16,1,
        16,1,16,1,17,1,17,1,17,1,17,5,17,251,8,17,10,17,12,17,254,9,17,1,
        17,1,17,1,18,1,18,1,18,1,18,1,18,1,18,5,18,264,8,18,10,18,12,18,
        267,9,18,1,18,1,18,1,19,1,19,1,19,1,19,1,19,1,19,5,19,277,8,19,10,
        19,12,19,280,9,19,1,19,1,19,5,19,284,8,19,10,19,12,19,287,9,19,3,
        19,289,8,19,1,19,3,19,292,8,19,3,19,294,8,19,1,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,3,20,304,8,20,1,21,1,21,1,21,1,21,5,21,310,8,
        21,10,21,12,21,313,9,21,1,21,1,21,1,22,1,22,1,22,1,22,3,22,321,8,
        22,1,23,1,23,1,23,1,23,5,23,327,8,23,10,23,12,23,330,9,23,1,23,1,
        23,1,24,1,24,1,24,1,24,1,24,5,24,339,8,24,10,24,12,24,342,9,24,1,
        24,3,24,345,8,24,1,25,1,25,1,25,1,25,1,25,1,25,5,25,353,8,25,10,
        25,12,25,356,9,25,1,25,1,25,1,26,1,26,1,26,1,26,5,26,364,8,26,10,
        26,12,26,367,9,26,1,26,1,26,1,27,1,27,1,27,1,27,5,27,375,8,27,10,
        27,12,27,378,9,27,1,27,1,27,1,28,1,28,1,28,1,28,5,28,386,8,28,10,
        28,12,28,389,9,28,1,28,1,28,1,29,1,29,1,29,1,29,5,29,397,8,29,10,
        29,12,29,400,9,29,1,29,1,29,1,30,1,30,1,30,1,30,1,30,1,30,3,30,410,
        8,30,1,30,1,30,1,30,1,30,1,30,5,30,417,8,30,10,30,12,30,420,9,30,
        1,30,3,30,423,8,30,1,30,1,30,1,30,1,30,1,30,5,30,430,8,30,10,30,
        12,30,433,9,30,1,30,3,30,436,8,30,1,30,1,30,1,30,1,30,1,30,1,30,
        1,30,1,30,1,30,3,30,447,8,30,1,30,3,30,450,8,30,1,31,1,31,1,31,1,
        31,5,31,456,8,31,10,31,12,31,459,9,31,1,31,1,31,1,32,1,32,1,32,1,
        32,5,32,467,8,32,10,32,12,32,470,9,32,1,32,1,32,1,33,1,33,1,33,1,
        33,5,33,478,8,33,10,33,12,33,481,9,33,1,33,1,33,1,34,1,34,1,34,1,
        34,5,34,489,8,34,10,34,12,34,492,9,34,1,34,1,34,1,35,1,35,3,35,498,
        8,35,1,36,1,36,1,36,1,36,5,36,504,8,36,10,36,12,36,507,9,36,1,36,
        1,36,1,37,1,37,3,37,513,8,37,1,38,1,38,1,38,1,38,1,38,5,38,520,8,
        38,10,38,12,38,523,9,38,1,38,3,38,526,8,38,1,39,1,39,1,39,5,39,531,
        8,39,10,39,12,39,534,9,39,1,40,1,40,1,40,3,40,539,8,40,1,40,3,40,
        542,8,40,1,40,1,40,1,40,1,40,1,40,3,40,549,8,40,1,40,3,40,552,8,
        40,3,40,554,8,40,1,41,1,41,1,41,5,41,559,8,41,10,41,12,41,562,9,
        41,1,42,1,42,1,43,1,43,1,44,1,44,1,44,1,44,5,44,572,8,44,10,44,12,
        44,575,9,44,1,45,1,45,1,45,1,45,1,45,1,45,3,45,583,8,45,1,46,1,46,
        1,46,0,0,47,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
        38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,
        82,84,86,88,90,92,0,5,1,0,57,58,2,0,41,41,46,46,2,0,29,29,33,38,
        1,0,54,58,1,0,40,43,630,0,95,1,0,0,0,2,105,1,0,0,0,4,112,1,0,0,0,
        6,121,1,0,0,0,8,151,1,0,0,0,10,153,1,0,0,0,12,157,1,0,0,0,14,169,
        1,0,0,0,16,171,1,0,0,0,18,186,1,0,0,0,20,191,1,0,0,0,22,194,1,0,
        0,0,24,197,1,0,0,0,26,224,1,0,0,0,28,227,1,0,0,0,30,238,1,0,0,0,
        32,242,1,0,0,0,34,246,1,0,0,0,36,257,1,0,0,0,38,293,1,0,0,0,40,295,
        1,0,0,0,42,305,1,0,0,0,44,316,1,0,0,0,46,322,1,0,0,0,48,333,1,0,
        0,0,50,346,1,0,0,0,52,359,1,0,0,0,54,370,1,0,0,0,56,381,1,0,0,0,
        58,392,1,0,0,0,60,449,1,0,0,0,62,451,1,0,0,0,64,462,1,0,0,0,66,473,
        1,0,0,0,68,484,1,0,0,0,70,497,1,0,0,0,72,499,1,0,0,0,74,512,1,0,
        0,0,76,514,1,0,0,0,78,527,1,0,0,0,80,553,1,0,0,0,82,555,1,0,0,0,
        84,563,1,0,0,0,86,565,1,0,0,0,88,567,1,0,0,0,90,582,1,0,0,0,92,584,
        1,0,0,0,94,96,3,2,1,0,95,94,1,0,0,0,95,96,1,0,0,0,96,100,1,0,0,0,
        97,99,3,8,4,0,98,97,1,0,0,0,99,102,1,0,0,0,100,98,1,0,0,0,100,101,
        1,0,0,0,101,103,1,0,0,0,102,100,1,0,0,0,103,104,5,0,0,1,104,1,1,
        0,0,0,105,107,5,1,0,0,106,108,7,0,0,0,107,106,1,0,0,0,107,108,1,
        0,0,0,108,110,1,0,0,0,109,111,3,4,2,0,110,109,1,0,0,0,110,111,1,
        0,0,0,111,3,1,0,0,0,112,116,5,50,0,0,113,115,3,6,3,0,114,113,1,0,
        0,0,115,118,1,0,0,0,116,114,1,0,0,0,116,117,1,0,0,0,117,119,1,0,
        0,0,118,116,1,0,0,0,119,120,5,51,0,0,120,5,1,0,0,0,121,122,5,57,
        0,0,122,123,5,44,0,0,123,128,3,86,43,0,124,125,5,45,0,0,125,127,
        3,86,43,0,126,124,1,0,0,0,127,130,1,0,0,0,128,126,1,0,0,0,128,129,
        1,0,0,0,129,132,1,0,0,0,130,128,1,0,0,0,131,133,5,47,0,0,132,131,
        1,0,0,0,132,133,1,0,0,0,133,7,1,0,0,0,134,152,3,10,5,0,135,152,3,
        20,10,0,136,152,3,34,17,0,137,152,3,28,14,0,138,152,3,36,18,0,139,
        152,3,42,21,0,140,152,3,46,23,0,141,152,3,50,25,0,142,152,3,52,26,
        0,143,152,3,54,27,0,144,152,3,56,28,0,145,152,3,58,29,0,146,152,
        3,62,31,0,147,152,3,64,32,0,148,152,3,66,33,0,149,152,3,68,34,0,
        150,152,3,72,36,0,151,134,1,0,0,0,151,135,1,0,0,0,151,136,1,0,0,
        0,151,137,1,0,0,0,151,138,1,0,0,0,151,139,1,0,0,0,151,140,1,0,0,
        0,151,141,1,0,0,0,151,142,1,0,0,0,151,143,1,0,0,0,151,144,1,0,0,
        0,151,145,1,0,0,0,151,146,1,0,0,0,151,147,1,0,0,0,151,148,1,0,0,
        0,151,149,1,0,0,0,151,150,1,0,0,0,152,9,1,0,0,0,153,154,5,2,0,0,
        154,155,5,57,0,0,155,156,3,12,6,0,156,11,1,0,0,0,157,161,5,50,0,
        0,158,160,3,14,7,0,159,158,1,0,0,0,160,163,1,0,0,0,161,159,1,0,0,
        0,161,162,1,0,0,0,162,164,1,0,0,0,163,161,1,0,0,0,164,165,5,51,0,
        0,165,13,1,0,0,0,166,170,3,16,8,0,167,170,3,18,9,0,168,170,3,28,
        14,0,169,166,1,0,0,0,169,167,1,0,0,0,169,168,1,0,0,0,170,15,1,0,
        0,0,171,172,5,57,0,0,172,173,5,44,0,0,173,175,3,24,12,0,174,176,
        3,22,11,0,175,174,1,0,0,0,175,176,1,0,0,0,176,180,1,0,0,0,177,179,
        3,26,13,0,178,177,1,0,0,0,179,182,1,0,0,0,180,178,1,0,0,0,180,181,
        1,0,0,0,181,184,1,0,0,0,182,180,1,0,0,0,183,185,5,47,0,0,184,183,
        1,0,0,0,184,185,1,0,0,0,185,17,1,0,0,0,186,187,5,30,0,0,187,189,
        5,57,0,0,188,190,5,47,0,0,189,188,1,0,0,0,189,190,1,0,0,0,190,19,
        1,0,0,0,191,192,5,57,0,0,192,193,3,12,6,0,193,21,1,0,0,0,194,195,
        5,39,0,0,195,196,3,88,44,0,196,23,1,0,0,0,197,201,5,57,0,0,198,199,
        5,48,0,0,199,200,5,56,0,0,200,202,5,49,0,0,201,198,1,0,0,0,201,202,
        1,0,0,0,202,205,1,0,0,0,203,204,5,52,0,0,204,206,5,53,0,0,205,203,
        1,0,0,0,205,206,1,0,0,0,206,25,1,0,0,0,207,225,5,23,0,0,208,225,
        5,24,0,0,209,225,5,25,0,0,210,225,5,26,0,0,211,225,5,27,0,0,212,
        213,5,28,0,0,213,225,3,86,43,0,214,215,5,3,0,0,215,217,3,32,16,0,
        216,218,3,30,15,0,217,216,1,0,0,0,217,218,1,0,0,0,218,225,1,0,0,
        0,219,220,5,32,0,0,220,222,3,32,16,0,221,223,3,30,15,0,222,221,1,
        0,0,0,222,223,1,0,0,0,223,225,1,0,0,0,224,207,1,0,0,0,224,208,1,
        0,0,0,224,209,1,0,0,0,224,210,1,0,0,0,224,211,1,0,0,0,224,212,1,
        0,0,0,224,214,1,0,0,0,224,219,1,0,0,0,225,27,1,0,0,0,226,228,5,3,
        0,0,227,226,1,0,0,0,227,228,1,0,0,0,228,229,1,0,0,0,229,230,3,32,
        16,0,230,231,5,32,0,0,231,233,3,32,16,0,232,234,3,30,15,0,233,232,
        1,0,0,0,233,234,1,0,0,0,234,236,1,0,0,0,235,237,5,47,0,0,236,235,
        1,0,0,0,236,237,1,0,0,0,237,29,1,0,0,0,238,239,5,52,0,0,239,240,
        3,78,39,0,240,241,5,53,0,0,241,31,1,0,0,0,242,243,5,57,0,0,243,244,
        5,46,0,0,244,245,5,57,0,0,245,33,1,0,0,0,246,247,5,4,0,0,247,248,
        5,57,0,0,248,252,5,50,0,0,249,251,5,57,0,0,250,249,1,0,0,0,251,254,
        1,0,0,0,252,250,1,0,0,0,252,253,1,0,0,0,253,255,1,0,0,0,254,252,
        1,0,0,0,255,256,5,51,0,0,256,35,1,0,0,0,257,258,5,5,0,0,258,259,
        5,57,0,0,259,260,5,6,0,0,260,261,5,57,0,0,261,265,5,50,0,0,262,264,
        3,38,19,0,263,262,1,0,0,0,264,267,1,0,0,0,265,263,1,0,0,0,265,266,
        1,0,0,0,266,268,1,0,0,0,267,265,1,0,0,0,268,269,5,51,0,0,269,37,
        1,0,0,0,270,294,3,40,20,0,271,288,5,57,0,0,272,273,5,44,0,0,273,
        278,5,57,0,0,274,275,5,45,0,0,275,277,5,57,0,0,276,274,1,0,0,0,277,
        280,1,0,0,0,278,276,1,0,0,0,278,279,1,0,0,0,279,289,1,0,0,0,280,
        278,1,0,0,0,281,282,5,45,0,0,282,284,5,57,0,0,283,281,1,0,0,0,284,
        287,1,0,0,0,285,283,1,0,0,0,285,286,1,0,0,0,286,289,1,0,0,0,287,
        285,1,0,0,0,288,272,1,0,0,0,288,285,1,0,0,0,289,291,1,0,0,0,290,
        292,5,47,0,0,291,290,1,0,0,0,291,292,1,0,0,0,292,294,1,0,0,0,293,
        270,1,0,0,0,293,271,1,0,0,0,294,39,1,0,0,0,295,296,5,31,0,0,296,
        297,5,57,0,0,297,298,5,57,0,0,298,299,5,56,0,0,299,300,5,56,0,0,
        300,301,5,56,0,0,301,303,5,56,0,0,302,304,5,47,0,0,303,302,1,0,0,
        0,303,304,1,0,0,0,304,41,1,0,0,0,305,306,5,7,0,0,306,307,5,57,0,
        0,307,311,5,50,0,0,308,310,3,44,22,0,309,308,1,0,0,0,310,313,1,0,
        0,0,311,309,1,0,0,0,311,312,1,0,0,0,312,314,1,0,0,0,313,311,1,0,
        0,0,314,315,5,51,0,0,315,43,1,0,0,0,316,317,5,57,0,0,317,318,5,32,
        0,0,318,320,5,57,0,0,319,321,5,47,0,0,320,319,1,0,0,0,320,321,1,
        0,0,0,321,45,1,0,0,0,322,323,5,8,0,0,323,324,5,57,0,0,324,328,5,
        50,0,0,325,327,3,48,24,0,326,325,1,0,0,0,327,330,1,0,0,0,328,326,
        1,0,0,0,328,329,1,0,0,0,329,331,1,0,0,0,330,328,1,0,0,0,331,332,
        5,51,0,0,332,47,1,0,0,0,333,334,5,57,0,0,334,335,5,44,0,0,335,340,
        5,57,0,0,336,337,5,45,0,0,337,339,5,57,0,0,338,336,1,0,0,0,339,342,
        1,0,0,0,340,338,1,0,0,0,340,341,1,0,0,0,341,344,1,0,0,0,342,340,
        1,0,0,0,343,345,5,47,0,0,344,343,1,0,0,0,344,345,1,0,0,0,345,49,
        1,0,0,0,346,347,5,9,0,0,347,348,5,57,0,0,348,349,5,6,0,0,349,350,
        5,57,0,0,350,354,5,50,0,0,351,353,3,80,40,0,352,351,1,0,0,0,353,
        356,1,0,0,0,354,352,1,0,0,0,354,355,1,0,0,0,355,357,1,0,0,0,356,
        354,1,0,0,0,357,358,5,51,0,0,358,51,1,0,0,0,359,360,5,21,0,0,360,
        361,5,57,0,0,361,365,5,50,0,0,362,364,3,76,38,0,363,362,1,0,0,0,
        364,367,1,0,0,0,365,363,1,0,0,0,365,366,1,0,0,0,366,368,1,0,0,0,
        367,365,1,0,0,0,368,369,5,51,0,0,369,53,1,0,0,0,370,371,5,22,0,0,
        371,372,5,57,0,0,372,376,5,50,0,0,373,375,3,76,38,0,374,373,1,0,
        0,0,375,378,1,0,0,0,376,374,1,0,0,0,376,377,1,0,0,0,377,379,1,0,
        0,0,378,376,1,0,0,0,379,380,5,51,0,0,380,55,1,0,0,0,381,382,5,10,
        0,0,382,383,5,57,0,0,383,387,5,50,0,0,384,386,3,76,38,0,385,384,
        1,0,0,0,386,389,1,0,0,0,387,385,1,0,0,0,387,388,1,0,0,0,388,390,
        1,0,0,0,389,387,1,0,0,0,390,391,5,51,0,0,391,57,1,0,0,0,392,393,
        5,11,0,0,393,394,5,57,0,0,394,398,5,50,0,0,395,397,3,60,30,0,396,
        395,1,0,0,0,397,400,1,0,0,0,398,396,1,0,0,0,398,399,1,0,0,0,399,
        401,1,0,0,0,400,398,1,0,0,0,401,402,5,51,0,0,402,59,1,0,0,0,403,
        404,5,17,0,0,404,405,5,10,0,0,405,406,5,57,0,0,406,407,5,14,0,0,
        407,409,3,78,39,0,408,410,5,47,0,0,409,408,1,0,0,0,409,410,1,0,0,
        0,410,450,1,0,0,0,411,412,5,18,0,0,412,413,5,57,0,0,413,418,3,78,
        39,0,414,415,5,45,0,0,415,417,3,78,39,0,416,414,1,0,0,0,417,420,
        1,0,0,0,418,416,1,0,0,0,418,419,1,0,0,0,419,422,1,0,0,0,420,418,
        1,0,0,0,421,423,5,47,0,0,422,421,1,0,0,0,422,423,1,0,0,0,423,450,
        1,0,0,0,424,425,5,19,0,0,425,426,5,57,0,0,426,431,3,78,39,0,427,
        428,5,45,0,0,428,430,3,78,39,0,429,427,1,0,0,0,430,433,1,0,0,0,431,
        429,1,0,0,0,431,432,1,0,0,0,432,435,1,0,0,0,433,431,1,0,0,0,434,
        436,5,47,0,0,435,434,1,0,0,0,435,436,1,0,0,0,436,450,1,0,0,0,437,
        438,5,20,0,0,438,439,5,57,0,0,439,440,5,57,0,0,440,441,5,57,0,0,
        441,442,5,32,0,0,442,443,5,57,0,0,443,444,5,57,0,0,444,446,5,57,
        0,0,445,447,5,47,0,0,446,445,1,0,0,0,446,447,1,0,0,0,447,450,1,0,
        0,0,448,450,3,76,38,0,449,403,1,0,0,0,449,411,1,0,0,0,449,424,1,
        0,0,0,449,437,1,0,0,0,449,448,1,0,0,0,450,61,1,0,0,0,451,452,5,12,
        0,0,452,453,5,57,0,0,453,457,5,50,0,0,454,456,3,76,38,0,455,454,
        1,0,0,0,456,459,1,0,0,0,457,455,1,0,0,0,457,458,1,0,0,0,458,460,
        1,0,0,0,459,457,1,0,0,0,460,461,5,51,0,0,461,63,1,0,0,0,462,463,
        5,13,0,0,463,464,5,57,0,0,464,468,5,50,0,0,465,467,3,76,38,0,466,
        465,1,0,0,0,467,470,1,0,0,0,468,466,1,0,0,0,468,469,1,0,0,0,469,
        471,1,0,0,0,470,468,1,0,0,0,471,472,5,51,0,0,472,65,1,0,0,0,473,
        474,5,14,0,0,474,475,5,57,0,0,475,479,5,50,0,0,476,478,3,76,38,0,
        477,476,1,0,0,0,478,481,1,0,0,0,479,477,1,0,0,0,479,480,1,0,0,0,
        480,482,1,0,0,0,481,479,1,0,0,0,482,483,5,51,0,0,483,67,1,0,0,0,
        484,485,5,15,0,0,485,486,5,57,0,0,486,490,5,50,0,0,487,489,3,70,
        35,0,488,487,1,0,0,0,489,492,1,0,0,0,490,488,1,0,0,0,490,491,1,0,
        0,0,491,493,1,0,0,0,492,490,1,0,0,0,493,494,5,51,0,0,494,69,1,0,
        0,0,495,498,3,44,22,0,496,498,3,76,38,0,497,495,1,0,0,0,497,496,
        1,0,0,0,498,71,1,0,0,0,499,500,5,16,0,0,500,501,5,57,0,0,501,505,
        5,50,0,0,502,504,3,74,37,0,503,502,1,0,0,0,504,507,1,0,0,0,505,503,
        1,0,0,0,505,506,1,0,0,0,506,508,1,0,0,0,507,505,1,0,0,0,508,509,
        5,51,0,0,509,73,1,0,0,0,510,513,3,48,24,0,511,513,3,76,38,0,512,
        510,1,0,0,0,512,511,1,0,0,0,513,75,1,0,0,0,514,515,5,57,0,0,515,
        516,5,44,0,0,516,521,3,78,39,0,517,518,5,45,0,0,518,520,3,78,39,
        0,519,517,1,0,0,0,520,523,1,0,0,0,521,519,1,0,0,0,521,522,1,0,0,
        0,522,525,1,0,0,0,523,521,1,0,0,0,524,526,5,47,0,0,525,524,1,0,0,
        0,525,526,1,0,0,0,526,77,1,0,0,0,527,532,3,86,43,0,528,529,7,1,0,
        0,529,531,3,86,43,0,530,528,1,0,0,0,531,534,1,0,0,0,532,530,1,0,
        0,0,532,533,1,0,0,0,533,79,1,0,0,0,534,532,1,0,0,0,535,536,5,57,
        0,0,536,538,5,24,0,0,537,539,5,58,0,0,538,537,1,0,0,0,538,539,1,
        0,0,0,539,541,1,0,0,0,540,542,5,47,0,0,541,540,1,0,0,0,541,542,1,
        0,0,0,542,554,1,0,0,0,543,544,5,57,0,0,544,545,3,84,42,0,545,548,
        3,82,41,0,546,547,5,32,0,0,547,549,5,57,0,0,548,546,1,0,0,0,548,
        549,1,0,0,0,549,551,1,0,0,0,550,552,5,47,0,0,551,550,1,0,0,0,551,
        552,1,0,0,0,552,554,1,0,0,0,553,535,1,0,0,0,553,543,1,0,0,0,554,
        81,1,0,0,0,555,560,3,86,43,0,556,557,5,45,0,0,557,559,3,86,43,0,
        558,556,1,0,0,0,559,562,1,0,0,0,560,558,1,0,0,0,560,561,1,0,0,0,
        561,83,1,0,0,0,562,560,1,0,0,0,563,564,7,2,0,0,564,85,1,0,0,0,565,
        566,7,3,0,0,566,87,1,0,0,0,567,573,3,90,45,0,568,569,3,92,46,0,569,
        570,3,90,45,0,570,572,1,0,0,0,571,568,1,0,0,0,572,575,1,0,0,0,573,
        571,1,0,0,0,573,574,1,0,0,0,574,89,1,0,0,0,575,573,1,0,0,0,576,583,
        3,32,16,0,577,583,3,86,43,0,578,579,5,48,0,0,579,580,3,88,44,0,580,
        581,5,49,0,0,581,583,1,0,0,0,582,576,1,0,0,0,582,577,1,0,0,0,582,
        578,1,0,0,0,583,91,1,0,0,0,584,585,7,4,0,0,585,93,1,0,0,0,65,95,
        100,107,110,116,128,132,151,161,169,175,180,184,189,201,205,217,
        222,224,227,233,236,252,265,278,285,288,291,293,303,311,320,328,
        340,344,354,365,376,387,398,409,418,422,431,435,446,449,457,468,
        479,490,497,505,512,521,525,532,538,541,548,551,553,560,573,582
    ]

class appgenParser ( Parser ):

    grammarFileName = "appgen.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'app'", "'table'", "'ref'", "'enum'",
                     "'view'", "'for'", "'flow'", "'role'", "'rule'", "'pbc'",
                     "'composition'", "'audit'", "'deploy'", "'version'",
                     "'operation'", "'security'", "'include'", "'require'",
                     "'expose'", "'connect'", "'llm'", "'agent'", "'pk'",
                     "'required'", "'unique'", "'hidden'", "'search'", "'default'",
                     "'in'", "'...'", "'@'", "'->'", "'=='", "'!='", "'>='",
                     "'<='", "'>'", "'<'", "'='", "'+'", "'-'", "'*'", "'/'",
                     "':'", "','", "'.'", "';'", "'('", "')'", "'{'", "'}'",
                     "'['", "']'" ]

    symbolicNames = [ "<INVALID>", "APP", "TABLE", "REF", "ENUM", "VIEW",
                      "FOR", "FLOW", "ROLE", "RULE", "PBC", "COMPOSITION",
                      "AUDIT", "DEPLOY", "VERSION", "OPERATION", "SECURITY",
                      "INCLUDE", "REQUIRE", "EXPOSE", "CONNECT", "LLM",
                      "AGENT", "PK", "REQUIRED", "UNIQUE", "HIDE", "SEARCH",
                      "DEFAULT", "IN", "ELLIPSIS", "AT", "ARROW", "EQEQ",
                      "NEQ", "GTE", "LTE", "GT", "LT", "EQ", "PLUS", "MINUS",
                      "STAR", "SLASH", "COLON", "COMMA", "DOT", "SEMI",
                      "LPAREN", "RPAREN", "LBRACE", "RBRACE", "LBRACK",
                      "RBRACK", "BOOL", "DECIMAL", "INT", "IDENT", "STRING",
                      "LINE_COMMENT", "BLOCK_COMMENT", "WS" ]

    RULE_schema = 0
    RULE_appDecl = 1
    RULE_appBlock = 2
    RULE_appOption = 3
    RULE_element = 4
    RULE_tableDecl = 5
    RULE_tableBody = 6
    RULE_tableItem = 7
    RULE_fieldDecl = 8
    RULE_spreadDecl = 9
    RULE_groupDecl = 10
    RULE_derivedExpr = 11
    RULE_typeRef = 12
    RULE_modifier = 13
    RULE_relationDecl = 14
    RULE_relationCardinality = 15
    RULE_target = 16
    RULE_enumDecl = 17
    RULE_viewDecl = 18
    RULE_viewItem = 19
    RULE_componentPlacement = 20
    RULE_flowDecl = 21
    RULE_flowStep = 22
    RULE_roleDecl = 23
    RULE_permission = 24
    RULE_ruleDecl = 25
    RULE_llmDecl = 26
    RULE_agentDecl = 27
    RULE_pbcDecl = 28
    RULE_compositionDecl = 29
    RULE_compositionItem = 30
    RULE_auditDecl = 31
    RULE_deploymentDecl = 32
    RULE_versionDecl = 33
    RULE_operationDecl = 34
    RULE_operationItem = 35
    RULE_securityDecl = 36
    RULE_securityItem = 37
    RULE_agenticOption = 38
    RULE_agenticValue = 39
    RULE_ruleItem = 40
    RULE_ruleValue = 41
    RULE_ruleOperator = 42
    RULE_literal = 43
    RULE_expression = 44
    RULE_expressionAtom = 45
    RULE_operator = 46

    ruleNames =  [ "schema", "appDecl", "appBlock", "appOption", "element",
                   "tableDecl", "tableBody", "tableItem", "fieldDecl", "spreadDecl",
                   "groupDecl", "derivedExpr", "typeRef", "modifier", "relationDecl",
                   "relationCardinality", "target", "enumDecl", "viewDecl",
                   "viewItem", "componentPlacement", "flowDecl", "flowStep",
                   "roleDecl", "permission", "ruleDecl", "llmDecl", "agentDecl",
                   "pbcDecl", "compositionDecl", "compositionItem", "auditDecl",
                   "deploymentDecl", "versionDecl", "operationDecl", "operationItem",
                   "securityDecl", "securityItem", "agenticOption", "agenticValue",
                   "ruleItem", "ruleValue", "ruleOperator", "literal", "expression",
                   "expressionAtom", "operator" ]

    EOF = Token.EOF
    APP=1
    TABLE=2
    REF=3
    ENUM=4
    VIEW=5
    FOR=6
    FLOW=7
    ROLE=8
    RULE=9
    PBC=10
    COMPOSITION=11
    AUDIT=12
    DEPLOY=13
    VERSION=14
    OPERATION=15
    SECURITY=16
    INCLUDE=17
    REQUIRE=18
    EXPOSE=19
    CONNECT=20
    LLM=21
    AGENT=22
    PK=23
    REQUIRED=24
    UNIQUE=25
    HIDE=26
    SEARCH=27
    DEFAULT=28
    IN=29
    ELLIPSIS=30
    AT=31
    ARROW=32
    EQEQ=33
    NEQ=34
    GTE=35
    LTE=36
    GT=37
    LT=38
    EQ=39
    PLUS=40
    MINUS=41
    STAR=42
    SLASH=43
    COLON=44
    COMMA=45
    DOT=46
    SEMI=47
    LPAREN=48
    RPAREN=49
    LBRACE=50
    RBRACE=51
    LBRACK=52
    RBRACK=53
    BOOL=54
    DECIMAL=55
    INT=56
    IDENT=57
    STRING=58
    LINE_COMMENT=59
    BLOCK_COMMENT=60
    WS=61

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SchemaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(appgenParser.EOF, 0)

        def appDecl(self):
            return self.getTypedRuleContext(appgenParser.AppDeclContext,0)


        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.ElementContext)
            else:
                return self.getTypedRuleContext(appgenParser.ElementContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_schema

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSchema" ):
                listener.enterSchema(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSchema" ):
                listener.exitSchema(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSchema" ):
                return visitor.visitSchema(self)
            else:
                return visitor.visitChildren(self)




    def schema(self):

        localctx = appgenParser.SchemaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_schema)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 94
                self.appDecl()


            self.state = 100
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 144115188082278332) != 0):
                self.state = 97
                self.element()
                self.state = 102
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 103
            self.match(appgenParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AppDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def APP(self):
            return self.getToken(appgenParser.APP, 0)

        def appBlock(self):
            return self.getTypedRuleContext(appgenParser.AppBlockContext,0)


        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def STRING(self):
            return self.getToken(appgenParser.STRING, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_appDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAppDecl" ):
                listener.enterAppDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAppDecl" ):
                listener.exitAppDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAppDecl" ):
                return visitor.visitAppDecl(self)
            else:
                return visitor.visitChildren(self)




    def appDecl(self):

        localctx = appgenParser.AppDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_appDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(appgenParser.APP)
            self.state = 107
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 106
                _la = self._input.LA(1)
                if not(_la==57 or _la==58):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==50:
                self.state = 109
                self.appBlock()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AppBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def appOption(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AppOptionContext)
            else:
                return self.getTypedRuleContext(appgenParser.AppOptionContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_appBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAppBlock" ):
                listener.enterAppBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAppBlock" ):
                listener.exitAppBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAppBlock" ):
                return visitor.visitAppBlock(self)
            else:
                return visitor.visitChildren(self)




    def appBlock(self):

        localctx = appgenParser.AppBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_appBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.match(appgenParser.LBRACE)
            self.state = 116
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 113
                self.appOption()
                self.state = 118
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 119
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AppOptionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def COLON(self):
            return self.getToken(appgenParser.COLON, 0)

        def literal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.LiteralContext)
            else:
                return self.getTypedRuleContext(appgenParser.LiteralContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.COMMA)
            else:
                return self.getToken(appgenParser.COMMA, i)

        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_appOption

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAppOption" ):
                listener.enterAppOption(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAppOption" ):
                listener.exitAppOption(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAppOption" ):
                return visitor.visitAppOption(self)
            else:
                return visitor.visitChildren(self)




    def appOption(self):

        localctx = appgenParser.AppOptionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_appOption)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 121
            self.match(appgenParser.IDENT)
            self.state = 122
            self.match(appgenParser.COLON)
            self.state = 123
            self.literal()
            self.state = 128
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==45:
                self.state = 124
                self.match(appgenParser.COMMA)
                self.state = 125
                self.literal()
                self.state = 130
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 132
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 131
                self.match(appgenParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tableDecl(self):
            return self.getTypedRuleContext(appgenParser.TableDeclContext,0)


        def groupDecl(self):
            return self.getTypedRuleContext(appgenParser.GroupDeclContext,0)


        def enumDecl(self):
            return self.getTypedRuleContext(appgenParser.EnumDeclContext,0)


        def relationDecl(self):
            return self.getTypedRuleContext(appgenParser.RelationDeclContext,0)


        def viewDecl(self):
            return self.getTypedRuleContext(appgenParser.ViewDeclContext,0)


        def flowDecl(self):
            return self.getTypedRuleContext(appgenParser.FlowDeclContext,0)


        def roleDecl(self):
            return self.getTypedRuleContext(appgenParser.RoleDeclContext,0)


        def ruleDecl(self):
            return self.getTypedRuleContext(appgenParser.RuleDeclContext,0)


        def llmDecl(self):
            return self.getTypedRuleContext(appgenParser.LlmDeclContext,0)


        def agentDecl(self):
            return self.getTypedRuleContext(appgenParser.AgentDeclContext,0)


        def pbcDecl(self):
            return self.getTypedRuleContext(appgenParser.PbcDeclContext,0)


        def compositionDecl(self):
            return self.getTypedRuleContext(appgenParser.CompositionDeclContext,0)


        def auditDecl(self):
            return self.getTypedRuleContext(appgenParser.AuditDeclContext,0)


        def deploymentDecl(self):
            return self.getTypedRuleContext(appgenParser.DeploymentDeclContext,0)


        def versionDecl(self):
            return self.getTypedRuleContext(appgenParser.VersionDeclContext,0)


        def operationDecl(self):
            return self.getTypedRuleContext(appgenParser.OperationDeclContext,0)


        def securityDecl(self):
            return self.getTypedRuleContext(appgenParser.SecurityDeclContext,0)


        def getRuleIndex(self):
            return appgenParser.RULE_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElement" ):
                listener.enterElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElement" ):
                listener.exitElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElement" ):
                return visitor.visitElement(self)
            else:
                return visitor.visitChildren(self)




    def element(self):

        localctx = appgenParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_element)
        try:
            self.state = 151
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 134
                self.tableDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 135
                self.groupDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 136
                self.enumDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 137
                self.relationDecl()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 138
                self.viewDecl()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 139
                self.flowDecl()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 140
                self.roleDecl()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 141
                self.ruleDecl()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 142
                self.llmDecl()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 143
                self.agentDecl()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 144
                self.pbcDecl()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 145
                self.compositionDecl()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 146
                self.auditDecl()
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 147
                self.deploymentDecl()
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 148
                self.versionDecl()
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 149
                self.operationDecl()
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 150
                self.securityDecl()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TableDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TABLE(self):
            return self.getToken(appgenParser.TABLE, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def tableBody(self):
            return self.getTypedRuleContext(appgenParser.TableBodyContext,0)


        def getRuleIndex(self):
            return appgenParser.RULE_tableDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTableDecl" ):
                listener.enterTableDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTableDecl" ):
                listener.exitTableDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTableDecl" ):
                return visitor.visitTableDecl(self)
            else:
                return visitor.visitChildren(self)




    def tableDecl(self):

        localctx = appgenParser.TableDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_tableDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            self.match(appgenParser.TABLE)
            self.state = 154
            self.match(appgenParser.IDENT)
            self.state = 155
            self.tableBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TableBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def tableItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.TableItemContext)
            else:
                return self.getTypedRuleContext(appgenParser.TableItemContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_tableBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTableBody" ):
                listener.enterTableBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTableBody" ):
                listener.exitTableBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTableBody" ):
                return visitor.visitTableBody(self)
            else:
                return visitor.visitChildren(self)




    def tableBody(self):

        localctx = appgenParser.TableBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_tableBody)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 157
            self.match(appgenParser.LBRACE)
            self.state = 161
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 144115189149597704) != 0):
                self.state = 158
                self.tableItem()
                self.state = 163
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 164
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TableItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fieldDecl(self):
            return self.getTypedRuleContext(appgenParser.FieldDeclContext,0)


        def spreadDecl(self):
            return self.getTypedRuleContext(appgenParser.SpreadDeclContext,0)


        def relationDecl(self):
            return self.getTypedRuleContext(appgenParser.RelationDeclContext,0)


        def getRuleIndex(self):
            return appgenParser.RULE_tableItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTableItem" ):
                listener.enterTableItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTableItem" ):
                listener.exitTableItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTableItem" ):
                return visitor.visitTableItem(self)
            else:
                return visitor.visitChildren(self)




    def tableItem(self):

        localctx = appgenParser.TableItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_tableItem)
        try:
            self.state = 169
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 166
                self.fieldDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 167
                self.spreadDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 168
                self.relationDecl()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def COLON(self):
            return self.getToken(appgenParser.COLON, 0)

        def typeRef(self):
            return self.getTypedRuleContext(appgenParser.TypeRefContext,0)


        def derivedExpr(self):
            return self.getTypedRuleContext(appgenParser.DerivedExprContext,0)


        def modifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.ModifierContext)
            else:
                return self.getTypedRuleContext(appgenParser.ModifierContext,i)


        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_fieldDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFieldDecl" ):
                listener.enterFieldDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFieldDecl" ):
                listener.exitFieldDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFieldDecl" ):
                return visitor.visitFieldDecl(self)
            else:
                return visitor.visitChildren(self)




    def fieldDecl(self):

        localctx = appgenParser.FieldDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_fieldDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self.match(appgenParser.IDENT)
            self.state = 172
            self.match(appgenParser.COLON)
            self.state = 173
            self.typeRef()
            self.state = 175
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 174
                self.derivedExpr()


            self.state = 180
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 177
                    self.modifier()
                self.state = 182
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

            self.state = 184
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 183
                self.match(appgenParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SpreadDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELLIPSIS(self):
            return self.getToken(appgenParser.ELLIPSIS, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_spreadDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpreadDecl" ):
                listener.enterSpreadDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpreadDecl" ):
                listener.exitSpreadDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSpreadDecl" ):
                return visitor.visitSpreadDecl(self)
            else:
                return visitor.visitChildren(self)




    def spreadDecl(self):

        localctx = appgenParser.SpreadDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_spreadDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.match(appgenParser.ELLIPSIS)
            self.state = 187
            self.match(appgenParser.IDENT)
            self.state = 189
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 188
                self.match(appgenParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def tableBody(self):
            return self.getTypedRuleContext(appgenParser.TableBodyContext,0)


        def getRuleIndex(self):
            return appgenParser.RULE_groupDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroupDecl" ):
                listener.enterGroupDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroupDecl" ):
                listener.exitGroupDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroupDecl" ):
                return visitor.visitGroupDecl(self)
            else:
                return visitor.visitChildren(self)




    def groupDecl(self):

        localctx = appgenParser.GroupDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_groupDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 191
            self.match(appgenParser.IDENT)
            self.state = 192
            self.tableBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DerivedExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(appgenParser.EQ, 0)

        def expression(self):
            return self.getTypedRuleContext(appgenParser.ExpressionContext,0)


        def getRuleIndex(self):
            return appgenParser.RULE_derivedExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDerivedExpr" ):
                listener.enterDerivedExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDerivedExpr" ):
                listener.exitDerivedExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDerivedExpr" ):
                return visitor.visitDerivedExpr(self)
            else:
                return visitor.visitChildren(self)




    def derivedExpr(self):

        localctx = appgenParser.DerivedExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_derivedExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.match(appgenParser.EQ)
            self.state = 195
            self.expression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(appgenParser.LPAREN, 0)

        def INT(self):
            return self.getToken(appgenParser.INT, 0)

        def RPAREN(self):
            return self.getToken(appgenParser.RPAREN, 0)

        def LBRACK(self):
            return self.getToken(appgenParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(appgenParser.RBRACK, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_typeRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeRef" ):
                listener.enterTypeRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeRef" ):
                listener.exitTypeRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeRef" ):
                return visitor.visitTypeRef(self)
            else:
                return visitor.visitChildren(self)




    def typeRef(self):

        localctx = appgenParser.TypeRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_typeRef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 197
            self.match(appgenParser.IDENT)
            self.state = 201
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==48:
                self.state = 198
                self.match(appgenParser.LPAREN)
                self.state = 199
                self.match(appgenParser.INT)
                self.state = 200
                self.match(appgenParser.RPAREN)


            self.state = 205
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 203
                self.match(appgenParser.LBRACK)
                self.state = 204
                self.match(appgenParser.RBRACK)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PK(self):
            return self.getToken(appgenParser.PK, 0)

        def REQUIRED(self):
            return self.getToken(appgenParser.REQUIRED, 0)

        def UNIQUE(self):
            return self.getToken(appgenParser.UNIQUE, 0)

        def HIDE(self):
            return self.getToken(appgenParser.HIDE, 0)

        def SEARCH(self):
            return self.getToken(appgenParser.SEARCH, 0)

        def DEFAULT(self):
            return self.getToken(appgenParser.DEFAULT, 0)

        def literal(self):
            return self.getTypedRuleContext(appgenParser.LiteralContext,0)


        def REF(self):
            return self.getToken(appgenParser.REF, 0)

        def target(self):
            return self.getTypedRuleContext(appgenParser.TargetContext,0)


        def relationCardinality(self):
            return self.getTypedRuleContext(appgenParser.RelationCardinalityContext,0)


        def ARROW(self):
            return self.getToken(appgenParser.ARROW, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_modifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModifier" ):
                listener.enterModifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModifier" ):
                listener.exitModifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModifier" ):
                return visitor.visitModifier(self)
            else:
                return visitor.visitChildren(self)




    def modifier(self):

        localctx = appgenParser.ModifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_modifier)
        self._la = 0 # Token type
        try:
            self.state = 224
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 207
                self.match(appgenParser.PK)
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 2)
                self.state = 208
                self.match(appgenParser.REQUIRED)
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 3)
                self.state = 209
                self.match(appgenParser.UNIQUE)
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 4)
                self.state = 210
                self.match(appgenParser.HIDE)
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 5)
                self.state = 211
                self.match(appgenParser.SEARCH)
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 6)
                self.state = 212
                self.match(appgenParser.DEFAULT)
                self.state = 213
                self.literal()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 7)
                self.state = 214
                self.match(appgenParser.REF)
                self.state = 215
                self.target()
                self.state = 217
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==52:
                    self.state = 216
                    self.relationCardinality()


                pass
            elif token in [32]:
                self.enterOuterAlt(localctx, 8)
                self.state = 219
                self.match(appgenParser.ARROW)
                self.state = 220
                self.target()
                self.state = 222
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==52:
                    self.state = 221
                    self.relationCardinality()


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def target(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.TargetContext)
            else:
                return self.getTypedRuleContext(appgenParser.TargetContext,i)


        def ARROW(self):
            return self.getToken(appgenParser.ARROW, 0)

        def REF(self):
            return self.getToken(appgenParser.REF, 0)

        def relationCardinality(self):
            return self.getTypedRuleContext(appgenParser.RelationCardinalityContext,0)


        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_relationDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationDecl" ):
                listener.enterRelationDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationDecl" ):
                listener.exitRelationDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationDecl" ):
                return visitor.visitRelationDecl(self)
            else:
                return visitor.visitChildren(self)




    def relationDecl(self):

        localctx = appgenParser.RelationDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_relationDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 227
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 226
                self.match(appgenParser.REF)


            self.state = 229
            self.target()
            self.state = 230
            self.match(appgenParser.ARROW)
            self.state = 231
            self.target()
            self.state = 233
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==52:
                self.state = 232
                self.relationCardinality()


            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 235
                self.match(appgenParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationCardinalityContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(appgenParser.LBRACK, 0)

        def agenticValue(self):
            return self.getTypedRuleContext(appgenParser.AgenticValueContext,0)


        def RBRACK(self):
            return self.getToken(appgenParser.RBRACK, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_relationCardinality

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationCardinality" ):
                listener.enterRelationCardinality(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationCardinality" ):
                listener.exitRelationCardinality(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationCardinality" ):
                return visitor.visitRelationCardinality(self)
            else:
                return visitor.visitChildren(self)




    def relationCardinality(self):

        localctx = appgenParser.RelationCardinalityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_relationCardinality)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self.match(appgenParser.LBRACK)
            self.state = 239
            self.agenticValue()
            self.state = 240
            self.match(appgenParser.RBRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TargetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def DOT(self):
            return self.getToken(appgenParser.DOT, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_target

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTarget" ):
                listener.enterTarget(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTarget" ):
                listener.exitTarget(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTarget" ):
                return visitor.visitTarget(self)
            else:
                return visitor.visitChildren(self)




    def target(self):

        localctx = appgenParser.TargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_target)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 242
            self.match(appgenParser.IDENT)
            self.state = 243
            self.match(appgenParser.DOT)
            self.state = 244
            self.match(appgenParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EnumDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENUM(self):
            return self.getToken(appgenParser.ENUM, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_enumDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnumDecl" ):
                listener.enterEnumDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnumDecl" ):
                listener.exitEnumDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnumDecl" ):
                return visitor.visitEnumDecl(self)
            else:
                return visitor.visitChildren(self)




    def enumDecl(self):

        localctx = appgenParser.EnumDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_enumDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 246
            self.match(appgenParser.ENUM)
            self.state = 247
            self.match(appgenParser.IDENT)
            self.state = 248
            self.match(appgenParser.LBRACE)
            self.state = 252
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 249
                self.match(appgenParser.IDENT)
                self.state = 254
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 255
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ViewDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VIEW(self):
            return self.getToken(appgenParser.VIEW, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def FOR(self):
            return self.getToken(appgenParser.FOR, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def viewItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.ViewItemContext)
            else:
                return self.getTypedRuleContext(appgenParser.ViewItemContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_viewDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterViewDecl" ):
                listener.enterViewDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitViewDecl" ):
                listener.exitViewDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitViewDecl" ):
                return visitor.visitViewDecl(self)
            else:
                return visitor.visitChildren(self)




    def viewDecl(self):

        localctx = appgenParser.ViewDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_viewDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            self.match(appgenParser.VIEW)
            self.state = 258
            self.match(appgenParser.IDENT)
            self.state = 259
            self.match(appgenParser.FOR)
            self.state = 260
            self.match(appgenParser.IDENT)
            self.state = 261
            self.match(appgenParser.LBRACE)
            self.state = 265
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==31 or _la==57:
                self.state = 262
                self.viewItem()
                self.state = 267
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 268
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ViewItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def componentPlacement(self):
            return self.getTypedRuleContext(appgenParser.ComponentPlacementContext,0)


        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def COLON(self):
            return self.getToken(appgenParser.COLON, 0)

        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.COMMA)
            else:
                return self.getToken(appgenParser.COMMA, i)

        def getRuleIndex(self):
            return appgenParser.RULE_viewItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterViewItem" ):
                listener.enterViewItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitViewItem" ):
                listener.exitViewItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitViewItem" ):
                return visitor.visitViewItem(self)
            else:
                return visitor.visitChildren(self)




    def viewItem(self):

        localctx = appgenParser.ViewItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_viewItem)
        self._la = 0 # Token type
        try:
            self.state = 293
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [31]:
                self.enterOuterAlt(localctx, 1)
                self.state = 270
                self.componentPlacement()
                pass
            elif token in [57]:
                self.enterOuterAlt(localctx, 2)
                self.state = 271
                self.match(appgenParser.IDENT)
                self.state = 288
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [44]:
                    self.state = 272
                    self.match(appgenParser.COLON)
                    self.state = 273
                    self.match(appgenParser.IDENT)
                    self.state = 278
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==45:
                        self.state = 274
                        self.match(appgenParser.COMMA)
                        self.state = 275
                        self.match(appgenParser.IDENT)
                        self.state = 280
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                elif token in [31, 45, 47, 51, 57]:
                    self.state = 285
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==45:
                        self.state = 281
                        self.match(appgenParser.COMMA)
                        self.state = 282
                        self.match(appgenParser.IDENT)
                        self.state = 287
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 291
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==47:
                    self.state = 290
                    self.match(appgenParser.SEMI)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComponentPlacementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AT(self):
            return self.getToken(appgenParser.AT, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.INT)
            else:
                return self.getToken(appgenParser.INT, i)

        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_componentPlacement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComponentPlacement" ):
                listener.enterComponentPlacement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComponentPlacement" ):
                listener.exitComponentPlacement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComponentPlacement" ):
                return visitor.visitComponentPlacement(self)
            else:
                return visitor.visitChildren(self)




    def componentPlacement(self):

        localctx = appgenParser.ComponentPlacementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_componentPlacement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 295
            self.match(appgenParser.AT)
            self.state = 296
            self.match(appgenParser.IDENT)
            self.state = 297
            self.match(appgenParser.IDENT)
            self.state = 298
            self.match(appgenParser.INT)
            self.state = 299
            self.match(appgenParser.INT)
            self.state = 300
            self.match(appgenParser.INT)
            self.state = 301
            self.match(appgenParser.INT)
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 302
                self.match(appgenParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FlowDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FLOW(self):
            return self.getToken(appgenParser.FLOW, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def flowStep(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.FlowStepContext)
            else:
                return self.getTypedRuleContext(appgenParser.FlowStepContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_flowDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFlowDecl" ):
                listener.enterFlowDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFlowDecl" ):
                listener.exitFlowDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFlowDecl" ):
                return visitor.visitFlowDecl(self)
            else:
                return visitor.visitChildren(self)




    def flowDecl(self):

        localctx = appgenParser.FlowDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_flowDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 305
            self.match(appgenParser.FLOW)
            self.state = 306
            self.match(appgenParser.IDENT)
            self.state = 307
            self.match(appgenParser.LBRACE)
            self.state = 311
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 308
                self.flowStep()
                self.state = 313
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 314
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FlowStepContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def ARROW(self):
            return self.getToken(appgenParser.ARROW, 0)

        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_flowStep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFlowStep" ):
                listener.enterFlowStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFlowStep" ):
                listener.exitFlowStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFlowStep" ):
                return visitor.visitFlowStep(self)
            else:
                return visitor.visitChildren(self)




    def flowStep(self):

        localctx = appgenParser.FlowStepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_flowStep)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 316
            self.match(appgenParser.IDENT)
            self.state = 317
            self.match(appgenParser.ARROW)
            self.state = 318
            self.match(appgenParser.IDENT)
            self.state = 320
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 319
                self.match(appgenParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RoleDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ROLE(self):
            return self.getToken(appgenParser.ROLE, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def permission(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.PermissionContext)
            else:
                return self.getTypedRuleContext(appgenParser.PermissionContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_roleDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoleDecl" ):
                listener.enterRoleDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoleDecl" ):
                listener.exitRoleDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoleDecl" ):
                return visitor.visitRoleDecl(self)
            else:
                return visitor.visitChildren(self)




    def roleDecl(self):

        localctx = appgenParser.RoleDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_roleDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 322
            self.match(appgenParser.ROLE)
            self.state = 323
            self.match(appgenParser.IDENT)
            self.state = 324
            self.match(appgenParser.LBRACE)
            self.state = 328
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 325
                self.permission()
                self.state = 330
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 331
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PermissionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def COLON(self):
            return self.getToken(appgenParser.COLON, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.COMMA)
            else:
                return self.getToken(appgenParser.COMMA, i)

        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_permission

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPermission" ):
                listener.enterPermission(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPermission" ):
                listener.exitPermission(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPermission" ):
                return visitor.visitPermission(self)
            else:
                return visitor.visitChildren(self)




    def permission(self):

        localctx = appgenParser.PermissionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_permission)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 333
            self.match(appgenParser.IDENT)
            self.state = 334
            self.match(appgenParser.COLON)
            self.state = 335
            self.match(appgenParser.IDENT)
            self.state = 340
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==45:
                self.state = 336
                self.match(appgenParser.COMMA)
                self.state = 337
                self.match(appgenParser.IDENT)
                self.state = 342
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 344
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 343
                self.match(appgenParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RULE(self):
            return self.getToken(appgenParser.RULE, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def FOR(self):
            return self.getToken(appgenParser.FOR, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def ruleItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.RuleItemContext)
            else:
                return self.getTypedRuleContext(appgenParser.RuleItemContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_ruleDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleDecl" ):
                listener.enterRuleDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleDecl" ):
                listener.exitRuleDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleDecl" ):
                return visitor.visitRuleDecl(self)
            else:
                return visitor.visitChildren(self)




    def ruleDecl(self):

        localctx = appgenParser.RuleDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_ruleDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 346
            self.match(appgenParser.RULE)
            self.state = 347
            self.match(appgenParser.IDENT)
            self.state = 348
            self.match(appgenParser.FOR)
            self.state = 349
            self.match(appgenParser.IDENT)
            self.state = 350
            self.match(appgenParser.LBRACE)
            self.state = 354
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 351
                self.ruleItem()
                self.state = 356
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 357
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LlmDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LLM(self):
            return self.getToken(appgenParser.LLM, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def agenticOption(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AgenticOptionContext)
            else:
                return self.getTypedRuleContext(appgenParser.AgenticOptionContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_llmDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLlmDecl" ):
                listener.enterLlmDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLlmDecl" ):
                listener.exitLlmDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLlmDecl" ):
                return visitor.visitLlmDecl(self)
            else:
                return visitor.visitChildren(self)




    def llmDecl(self):

        localctx = appgenParser.LlmDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_llmDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 359
            self.match(appgenParser.LLM)
            self.state = 360
            self.match(appgenParser.IDENT)
            self.state = 361
            self.match(appgenParser.LBRACE)
            self.state = 365
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 362
                self.agenticOption()
                self.state = 367
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 368
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AgentDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AGENT(self):
            return self.getToken(appgenParser.AGENT, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def agenticOption(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AgenticOptionContext)
            else:
                return self.getTypedRuleContext(appgenParser.AgenticOptionContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_agentDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAgentDecl" ):
                listener.enterAgentDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAgentDecl" ):
                listener.exitAgentDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAgentDecl" ):
                return visitor.visitAgentDecl(self)
            else:
                return visitor.visitChildren(self)




    def agentDecl(self):

        localctx = appgenParser.AgentDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_agentDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 370
            self.match(appgenParser.AGENT)
            self.state = 371
            self.match(appgenParser.IDENT)
            self.state = 372
            self.match(appgenParser.LBRACE)
            self.state = 376
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 373
                self.agenticOption()
                self.state = 378
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 379
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PbcDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PBC(self):
            return self.getToken(appgenParser.PBC, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def agenticOption(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AgenticOptionContext)
            else:
                return self.getTypedRuleContext(appgenParser.AgenticOptionContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_pbcDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPbcDecl" ):
                listener.enterPbcDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPbcDecl" ):
                listener.exitPbcDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPbcDecl" ):
                return visitor.visitPbcDecl(self)
            else:
                return visitor.visitChildren(self)




    def pbcDecl(self):

        localctx = appgenParser.PbcDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_pbcDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
            self.match(appgenParser.PBC)
            self.state = 382
            self.match(appgenParser.IDENT)
            self.state = 383
            self.match(appgenParser.LBRACE)
            self.state = 387
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 384
                self.agenticOption()
                self.state = 389
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 390
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompositionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMPOSITION(self):
            return self.getToken(appgenParser.COMPOSITION, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def compositionItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.CompositionItemContext)
            else:
                return self.getTypedRuleContext(appgenParser.CompositionItemContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_compositionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompositionDecl" ):
                listener.enterCompositionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompositionDecl" ):
                listener.exitCompositionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompositionDecl" ):
                return visitor.visitCompositionDecl(self)
            else:
                return visitor.visitChildren(self)




    def compositionDecl(self):

        localctx = appgenParser.CompositionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_compositionDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 392
            self.match(appgenParser.COMPOSITION)
            self.state = 393
            self.match(appgenParser.IDENT)
            self.state = 394
            self.match(appgenParser.LBRACE)
            self.state = 398
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 144115188077821952) != 0):
                self.state = 395
                self.compositionItem()
                self.state = 400
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 401
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompositionItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INCLUDE(self):
            return self.getToken(appgenParser.INCLUDE, 0)

        def PBC(self):
            return self.getToken(appgenParser.PBC, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def VERSION(self):
            return self.getToken(appgenParser.VERSION, 0)

        def agenticValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AgenticValueContext)
            else:
                return self.getTypedRuleContext(appgenParser.AgenticValueContext,i)


        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def REQUIRE(self):
            return self.getToken(appgenParser.REQUIRE, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.COMMA)
            else:
                return self.getToken(appgenParser.COMMA, i)

        def EXPOSE(self):
            return self.getToken(appgenParser.EXPOSE, 0)

        def CONNECT(self):
            return self.getToken(appgenParser.CONNECT, 0)

        def ARROW(self):
            return self.getToken(appgenParser.ARROW, 0)

        def agenticOption(self):
            return self.getTypedRuleContext(appgenParser.AgenticOptionContext,0)


        def getRuleIndex(self):
            return appgenParser.RULE_compositionItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompositionItem" ):
                listener.enterCompositionItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompositionItem" ):
                listener.exitCompositionItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompositionItem" ):
                return visitor.visitCompositionItem(self)
            else:
                return visitor.visitChildren(self)




    def compositionItem(self):

        localctx = appgenParser.CompositionItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_compositionItem)
        self._la = 0 # Token type
        try:
            self.state = 449
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 403
                self.match(appgenParser.INCLUDE)
                self.state = 404
                self.match(appgenParser.PBC)
                self.state = 405
                self.match(appgenParser.IDENT)
                self.state = 406
                self.match(appgenParser.VERSION)
                self.state = 407
                self.agenticValue()
                self.state = 409
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==47:
                    self.state = 408
                    self.match(appgenParser.SEMI)


                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 411
                self.match(appgenParser.REQUIRE)
                self.state = 412
                self.match(appgenParser.IDENT)
                self.state = 413
                self.agenticValue()
                self.state = 418
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==45:
                    self.state = 414
                    self.match(appgenParser.COMMA)
                    self.state = 415
                    self.agenticValue()
                    self.state = 420
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 422
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==47:
                    self.state = 421
                    self.match(appgenParser.SEMI)


                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 3)
                self.state = 424
                self.match(appgenParser.EXPOSE)
                self.state = 425
                self.match(appgenParser.IDENT)
                self.state = 426
                self.agenticValue()
                self.state = 431
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==45:
                    self.state = 427
                    self.match(appgenParser.COMMA)
                    self.state = 428
                    self.agenticValue()
                    self.state = 433
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 435
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==47:
                    self.state = 434
                    self.match(appgenParser.SEMI)


                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 4)
                self.state = 437
                self.match(appgenParser.CONNECT)
                self.state = 438
                self.match(appgenParser.IDENT)
                self.state = 439
                self.match(appgenParser.IDENT)
                self.state = 440
                self.match(appgenParser.IDENT)
                self.state = 441
                self.match(appgenParser.ARROW)
                self.state = 442
                self.match(appgenParser.IDENT)
                self.state = 443
                self.match(appgenParser.IDENT)
                self.state = 444
                self.match(appgenParser.IDENT)
                self.state = 446
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==47:
                    self.state = 445
                    self.match(appgenParser.SEMI)


                pass
            elif token in [57]:
                self.enterOuterAlt(localctx, 5)
                self.state = 448
                self.agenticOption()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AuditDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AUDIT(self):
            return self.getToken(appgenParser.AUDIT, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def agenticOption(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AgenticOptionContext)
            else:
                return self.getTypedRuleContext(appgenParser.AgenticOptionContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_auditDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAuditDecl" ):
                listener.enterAuditDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAuditDecl" ):
                listener.exitAuditDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAuditDecl" ):
                return visitor.visitAuditDecl(self)
            else:
                return visitor.visitChildren(self)




    def auditDecl(self):

        localctx = appgenParser.AuditDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_auditDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 451
            self.match(appgenParser.AUDIT)
            self.state = 452
            self.match(appgenParser.IDENT)
            self.state = 453
            self.match(appgenParser.LBRACE)
            self.state = 457
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 454
                self.agenticOption()
                self.state = 459
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 460
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeploymentDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEPLOY(self):
            return self.getToken(appgenParser.DEPLOY, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def agenticOption(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AgenticOptionContext)
            else:
                return self.getTypedRuleContext(appgenParser.AgenticOptionContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_deploymentDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeploymentDecl" ):
                listener.enterDeploymentDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeploymentDecl" ):
                listener.exitDeploymentDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeploymentDecl" ):
                return visitor.visitDeploymentDecl(self)
            else:
                return visitor.visitChildren(self)




    def deploymentDecl(self):

        localctx = appgenParser.DeploymentDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_deploymentDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 462
            self.match(appgenParser.DEPLOY)
            self.state = 463
            self.match(appgenParser.IDENT)
            self.state = 464
            self.match(appgenParser.LBRACE)
            self.state = 468
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 465
                self.agenticOption()
                self.state = 470
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 471
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VersionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VERSION(self):
            return self.getToken(appgenParser.VERSION, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def agenticOption(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AgenticOptionContext)
            else:
                return self.getTypedRuleContext(appgenParser.AgenticOptionContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_versionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVersionDecl" ):
                listener.enterVersionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVersionDecl" ):
                listener.exitVersionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVersionDecl" ):
                return visitor.visitVersionDecl(self)
            else:
                return visitor.visitChildren(self)




    def versionDecl(self):

        localctx = appgenParser.VersionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_versionDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 473
            self.match(appgenParser.VERSION)
            self.state = 474
            self.match(appgenParser.IDENT)
            self.state = 475
            self.match(appgenParser.LBRACE)
            self.state = 479
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 476
                self.agenticOption()
                self.state = 481
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 482
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperationDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPERATION(self):
            return self.getToken(appgenParser.OPERATION, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def operationItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.OperationItemContext)
            else:
                return self.getTypedRuleContext(appgenParser.OperationItemContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_operationDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperationDecl" ):
                listener.enterOperationDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperationDecl" ):
                listener.exitOperationDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperationDecl" ):
                return visitor.visitOperationDecl(self)
            else:
                return visitor.visitChildren(self)




    def operationDecl(self):

        localctx = appgenParser.OperationDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_operationDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 484
            self.match(appgenParser.OPERATION)
            self.state = 485
            self.match(appgenParser.IDENT)
            self.state = 486
            self.match(appgenParser.LBRACE)
            self.state = 490
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 487
                self.operationItem()
                self.state = 492
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 493
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperationItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def flowStep(self):
            return self.getTypedRuleContext(appgenParser.FlowStepContext,0)


        def agenticOption(self):
            return self.getTypedRuleContext(appgenParser.AgenticOptionContext,0)


        def getRuleIndex(self):
            return appgenParser.RULE_operationItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperationItem" ):
                listener.enterOperationItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperationItem" ):
                listener.exitOperationItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperationItem" ):
                return visitor.visitOperationItem(self)
            else:
                return visitor.visitChildren(self)




    def operationItem(self):

        localctx = appgenParser.OperationItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_operationItem)
        try:
            self.state = 497
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,51,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 495
                self.flowStep()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 496
                self.agenticOption()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SecurityDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SECURITY(self):
            return self.getToken(appgenParser.SECURITY, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def LBRACE(self):
            return self.getToken(appgenParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(appgenParser.RBRACE, 0)

        def securityItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.SecurityItemContext)
            else:
                return self.getTypedRuleContext(appgenParser.SecurityItemContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_securityDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSecurityDecl" ):
                listener.enterSecurityDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSecurityDecl" ):
                listener.exitSecurityDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSecurityDecl" ):
                return visitor.visitSecurityDecl(self)
            else:
                return visitor.visitChildren(self)




    def securityDecl(self):

        localctx = appgenParser.SecurityDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_securityDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 499
            self.match(appgenParser.SECURITY)
            self.state = 500
            self.match(appgenParser.IDENT)
            self.state = 501
            self.match(appgenParser.LBRACE)
            self.state = 505
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==57:
                self.state = 502
                self.securityItem()
                self.state = 507
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 508
            self.match(appgenParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SecurityItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def permission(self):
            return self.getTypedRuleContext(appgenParser.PermissionContext,0)


        def agenticOption(self):
            return self.getTypedRuleContext(appgenParser.AgenticOptionContext,0)


        def getRuleIndex(self):
            return appgenParser.RULE_securityItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSecurityItem" ):
                listener.enterSecurityItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSecurityItem" ):
                listener.exitSecurityItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSecurityItem" ):
                return visitor.visitSecurityItem(self)
            else:
                return visitor.visitChildren(self)




    def securityItem(self):

        localctx = appgenParser.SecurityItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_securityItem)
        try:
            self.state = 512
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,53,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 510
                self.permission()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 511
                self.agenticOption()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AgenticOptionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def COLON(self):
            return self.getToken(appgenParser.COLON, 0)

        def agenticValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.AgenticValueContext)
            else:
                return self.getTypedRuleContext(appgenParser.AgenticValueContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.COMMA)
            else:
                return self.getToken(appgenParser.COMMA, i)

        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_agenticOption

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAgenticOption" ):
                listener.enterAgenticOption(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAgenticOption" ):
                listener.exitAgenticOption(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAgenticOption" ):
                return visitor.visitAgenticOption(self)
            else:
                return visitor.visitChildren(self)




    def agenticOption(self):

        localctx = appgenParser.AgenticOptionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_agenticOption)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 514
            self.match(appgenParser.IDENT)
            self.state = 515
            self.match(appgenParser.COLON)
            self.state = 516
            self.agenticValue()
            self.state = 521
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==45:
                self.state = 517
                self.match(appgenParser.COMMA)
                self.state = 518
                self.agenticValue()
                self.state = 523
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 525
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==47:
                self.state = 524
                self.match(appgenParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AgenticValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.LiteralContext)
            else:
                return self.getTypedRuleContext(appgenParser.LiteralContext,i)


        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.DOT)
            else:
                return self.getToken(appgenParser.DOT, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.MINUS)
            else:
                return self.getToken(appgenParser.MINUS, i)

        def getRuleIndex(self):
            return appgenParser.RULE_agenticValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAgenticValue" ):
                listener.enterAgenticValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAgenticValue" ):
                listener.exitAgenticValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAgenticValue" ):
                return visitor.visitAgenticValue(self)
            else:
                return visitor.visitChildren(self)




    def agenticValue(self):

        localctx = appgenParser.AgenticValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_agenticValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 527
            self.literal()
            self.state = 532
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==41 or _la==46:
                self.state = 528
                _la = self._input.LA(1)
                if not(_la==41 or _la==46):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 529
                self.literal()
                self.state = 534
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.IDENT)
            else:
                return self.getToken(appgenParser.IDENT, i)

        def REQUIRED(self):
            return self.getToken(appgenParser.REQUIRED, 0)

        def STRING(self):
            return self.getToken(appgenParser.STRING, 0)

        def SEMI(self):
            return self.getToken(appgenParser.SEMI, 0)

        def ruleOperator(self):
            return self.getTypedRuleContext(appgenParser.RuleOperatorContext,0)


        def ruleValue(self):
            return self.getTypedRuleContext(appgenParser.RuleValueContext,0)


        def ARROW(self):
            return self.getToken(appgenParser.ARROW, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_ruleItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleItem" ):
                listener.enterRuleItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleItem" ):
                listener.exitRuleItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleItem" ):
                return visitor.visitRuleItem(self)
            else:
                return visitor.visitChildren(self)




    def ruleItem(self):

        localctx = appgenParser.RuleItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_ruleItem)
        self._la = 0 # Token type
        try:
            self.state = 553
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,61,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 535
                self.match(appgenParser.IDENT)
                self.state = 536
                self.match(appgenParser.REQUIRED)
                self.state = 538
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==58:
                    self.state = 537
                    self.match(appgenParser.STRING)


                self.state = 541
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==47:
                    self.state = 540
                    self.match(appgenParser.SEMI)


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 543
                self.match(appgenParser.IDENT)
                self.state = 544
                self.ruleOperator()
                self.state = 545
                self.ruleValue()
                self.state = 548
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==32:
                    self.state = 546
                    self.match(appgenParser.ARROW)
                    self.state = 547
                    self.match(appgenParser.IDENT)


                self.state = 551
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==47:
                    self.state = 550
                    self.match(appgenParser.SEMI)


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.LiteralContext)
            else:
                return self.getTypedRuleContext(appgenParser.LiteralContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(appgenParser.COMMA)
            else:
                return self.getToken(appgenParser.COMMA, i)

        def getRuleIndex(self):
            return appgenParser.RULE_ruleValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleValue" ):
                listener.enterRuleValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleValue" ):
                listener.exitRuleValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleValue" ):
                return visitor.visitRuleValue(self)
            else:
                return visitor.visitChildren(self)




    def ruleValue(self):

        localctx = appgenParser.RuleValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_ruleValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 555
            self.literal()
            self.state = 560
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==45:
                self.state = 556
                self.match(appgenParser.COMMA)
                self.state = 557
                self.literal()
                self.state = 562
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQEQ(self):
            return self.getToken(appgenParser.EQEQ, 0)

        def NEQ(self):
            return self.getToken(appgenParser.NEQ, 0)

        def GTE(self):
            return self.getToken(appgenParser.GTE, 0)

        def LTE(self):
            return self.getToken(appgenParser.LTE, 0)

        def GT(self):
            return self.getToken(appgenParser.GT, 0)

        def LT(self):
            return self.getToken(appgenParser.LT, 0)

        def IN(self):
            return self.getToken(appgenParser.IN, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_ruleOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleOperator" ):
                listener.enterRuleOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleOperator" ):
                listener.exitRuleOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRuleOperator" ):
                return visitor.visitRuleOperator(self)
            else:
                return visitor.visitChildren(self)




    def ruleOperator(self):

        localctx = appgenParser.RuleOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_ruleOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 563
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 541702750208) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(appgenParser.STRING, 0)

        def DECIMAL(self):
            return self.getToken(appgenParser.DECIMAL, 0)

        def INT(self):
            return self.getToken(appgenParser.INT, 0)

        def BOOL(self):
            return self.getToken(appgenParser.BOOL, 0)

        def IDENT(self):
            return self.getToken(appgenParser.IDENT, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = appgenParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 565
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 558446353793941504) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expressionAtom(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.ExpressionAtomContext)
            else:
                return self.getTypedRuleContext(appgenParser.ExpressionAtomContext,i)


        def operator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(appgenParser.OperatorContext)
            else:
                return self.getTypedRuleContext(appgenParser.OperatorContext,i)


        def getRuleIndex(self):
            return appgenParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = appgenParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 567
            self.expressionAtom()
            self.state = 573
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 16492674416640) != 0):
                self.state = 568
                self.operator()
                self.state = 569
                self.expressionAtom()
                self.state = 575
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionAtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def target(self):
            return self.getTypedRuleContext(appgenParser.TargetContext,0)


        def literal(self):
            return self.getTypedRuleContext(appgenParser.LiteralContext,0)


        def LPAREN(self):
            return self.getToken(appgenParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(appgenParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(appgenParser.RPAREN, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_expressionAtom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpressionAtom" ):
                listener.enterExpressionAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpressionAtom" ):
                listener.exitExpressionAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionAtom" ):
                return visitor.visitExpressionAtom(self)
            else:
                return visitor.visitChildren(self)




    def expressionAtom(self):

        localctx = appgenParser.ExpressionAtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_expressionAtom)
        try:
            self.state = 582
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,64,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 576
                self.target()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 577
                self.literal()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 578
                self.match(appgenParser.LPAREN)
                self.state = 579
                self.expression()
                self.state = 580
                self.match(appgenParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(appgenParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(appgenParser.MINUS, 0)

        def STAR(self):
            return self.getToken(appgenParser.STAR, 0)

        def SLASH(self):
            return self.getToken(appgenParser.SLASH, 0)

        def getRuleIndex(self):
            return appgenParser.RULE_operator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperator" ):
                listener.enterOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperator" ):
                listener.exitOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperator" ):
                return visitor.visitOperator(self)
            else:
                return visitor.visitChildren(self)




    def operator(self):

        localctx = appgenParser.OperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_operator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 584
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 16492674416640) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





