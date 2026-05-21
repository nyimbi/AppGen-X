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
        4,1,50,427,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,1,0,3,0,76,8,0,1,0,5,0,79,8,0,
        10,0,12,0,82,9,0,1,0,1,0,1,1,1,1,3,1,88,8,1,1,1,3,1,91,8,1,1,2,1,
        2,5,2,95,8,2,10,2,12,2,98,9,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,5,3,107,
        8,3,10,3,12,3,110,9,3,1,3,3,3,113,8,3,1,4,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,4,1,4,3,4,125,8,4,1,5,1,5,1,5,1,5,1,6,1,6,5,6,133,8,6,10,
        6,12,6,136,9,6,1,6,1,6,1,7,1,7,1,7,3,7,143,8,7,1,8,1,8,1,8,1,8,3,
        8,149,8,8,1,8,5,8,152,8,8,10,8,12,8,155,9,8,1,8,3,8,158,8,8,1,9,
        1,9,1,9,3,9,163,8,9,1,10,1,10,1,10,1,11,1,11,1,11,1,12,1,12,1,12,
        1,12,3,12,175,8,12,1,12,1,12,3,12,179,8,12,1,13,1,13,1,13,1,13,1,
        13,1,13,1,13,1,13,1,13,1,13,3,13,191,8,13,1,13,1,13,1,13,3,13,196,
        8,13,3,13,198,8,13,1,14,3,14,201,8,14,1,14,1,14,1,14,1,14,3,14,207,
        8,14,1,14,3,14,210,8,14,1,15,1,15,1,15,1,15,1,16,1,16,1,16,1,16,
        1,17,1,17,1,17,1,17,5,17,224,8,17,10,17,12,17,227,9,17,1,17,1,17,
        1,18,1,18,1,18,1,18,1,18,1,18,5,18,237,8,18,10,18,12,18,240,9,18,
        1,18,1,18,1,19,1,19,1,19,1,19,1,19,1,19,5,19,250,8,19,10,19,12,19,
        253,9,19,1,19,1,19,5,19,257,8,19,10,19,12,19,260,9,19,3,19,262,8,
        19,1,19,3,19,265,8,19,3,19,267,8,19,1,20,1,20,1,20,1,20,1,20,1,20,
        1,20,1,20,3,20,277,8,20,1,21,1,21,1,21,1,21,5,21,283,8,21,10,21,
        12,21,286,9,21,1,21,1,21,1,22,1,22,1,22,1,22,3,22,294,8,22,1,23,
        1,23,1,23,1,23,5,23,300,8,23,10,23,12,23,303,9,23,1,23,1,23,1,24,
        1,24,1,24,1,24,1,24,5,24,312,8,24,10,24,12,24,315,9,24,1,24,3,24,
        318,8,24,1,25,1,25,1,25,1,25,1,25,1,25,5,25,326,8,25,10,25,12,25,
        329,9,25,1,25,1,25,1,26,1,26,1,26,1,26,5,26,337,8,26,10,26,12,26,
        340,9,26,1,26,1,26,1,27,1,27,1,27,1,27,5,27,348,8,27,10,27,12,27,
        351,9,27,1,27,1,27,1,28,1,28,1,28,1,28,1,28,5,28,360,8,28,10,28,
        12,28,363,9,28,1,28,3,28,366,8,28,1,29,1,29,1,29,5,29,371,8,29,10,
        29,12,29,374,9,29,1,30,1,30,1,30,3,30,379,8,30,1,30,3,30,382,8,30,
        1,30,1,30,1,30,1,30,1,30,3,30,389,8,30,1,30,3,30,392,8,30,3,30,394,
        8,30,1,31,1,31,1,31,5,31,399,8,31,10,31,12,31,402,9,31,1,32,1,32,
        1,33,1,33,1,34,1,34,1,34,1,34,5,34,412,8,34,10,34,12,34,415,9,34,
        1,35,1,35,1,35,1,35,1,35,1,35,3,35,423,8,35,1,36,1,36,1,36,0,0,37,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,
        46,48,50,52,54,56,58,60,62,64,66,68,70,72,0,5,1,0,46,47,2,0,30,30,
        35,35,2,0,18,18,22,27,1,0,43,47,1,0,29,32,454,0,75,1,0,0,0,2,85,
        1,0,0,0,4,92,1,0,0,0,6,101,1,0,0,0,8,124,1,0,0,0,10,126,1,0,0,0,
        12,130,1,0,0,0,14,142,1,0,0,0,16,144,1,0,0,0,18,159,1,0,0,0,20,164,
        1,0,0,0,22,167,1,0,0,0,24,170,1,0,0,0,26,197,1,0,0,0,28,200,1,0,
        0,0,30,211,1,0,0,0,32,215,1,0,0,0,34,219,1,0,0,0,36,230,1,0,0,0,
        38,266,1,0,0,0,40,268,1,0,0,0,42,278,1,0,0,0,44,289,1,0,0,0,46,295,
        1,0,0,0,48,306,1,0,0,0,50,319,1,0,0,0,52,332,1,0,0,0,54,343,1,0,
        0,0,56,354,1,0,0,0,58,367,1,0,0,0,60,393,1,0,0,0,62,395,1,0,0,0,
        64,403,1,0,0,0,66,405,1,0,0,0,68,407,1,0,0,0,70,422,1,0,0,0,72,424,
        1,0,0,0,74,76,3,2,1,0,75,74,1,0,0,0,75,76,1,0,0,0,76,80,1,0,0,0,
        77,79,3,8,4,0,78,77,1,0,0,0,79,82,1,0,0,0,80,78,1,0,0,0,80,81,1,
        0,0,0,81,83,1,0,0,0,82,80,1,0,0,0,83,84,5,0,0,1,84,1,1,0,0,0,85,
        87,5,1,0,0,86,88,7,0,0,0,87,86,1,0,0,0,87,88,1,0,0,0,88,90,1,0,0,
        0,89,91,3,4,2,0,90,89,1,0,0,0,90,91,1,0,0,0,91,3,1,0,0,0,92,96,5,
        39,0,0,93,95,3,6,3,0,94,93,1,0,0,0,95,98,1,0,0,0,96,94,1,0,0,0,96,
        97,1,0,0,0,97,99,1,0,0,0,98,96,1,0,0,0,99,100,5,40,0,0,100,5,1,0,
        0,0,101,102,5,46,0,0,102,103,5,33,0,0,103,108,3,66,33,0,104,105,
        5,34,0,0,105,107,3,66,33,0,106,104,1,0,0,0,107,110,1,0,0,0,108,106,
        1,0,0,0,108,109,1,0,0,0,109,112,1,0,0,0,110,108,1,0,0,0,111,113,
        5,36,0,0,112,111,1,0,0,0,112,113,1,0,0,0,113,7,1,0,0,0,114,125,3,
        10,5,0,115,125,3,20,10,0,116,125,3,34,17,0,117,125,3,28,14,0,118,
        125,3,36,18,0,119,125,3,42,21,0,120,125,3,46,23,0,121,125,3,50,25,
        0,122,125,3,52,26,0,123,125,3,54,27,0,124,114,1,0,0,0,124,115,1,
        0,0,0,124,116,1,0,0,0,124,117,1,0,0,0,124,118,1,0,0,0,124,119,1,
        0,0,0,124,120,1,0,0,0,124,121,1,0,0,0,124,122,1,0,0,0,124,123,1,
        0,0,0,125,9,1,0,0,0,126,127,5,2,0,0,127,128,5,46,0,0,128,129,3,12,
        6,0,129,11,1,0,0,0,130,134,5,39,0,0,131,133,3,14,7,0,132,131,1,0,
        0,0,133,136,1,0,0,0,134,132,1,0,0,0,134,135,1,0,0,0,135,137,1,0,
        0,0,136,134,1,0,0,0,137,138,5,40,0,0,138,13,1,0,0,0,139,143,3,16,
        8,0,140,143,3,18,9,0,141,143,3,28,14,0,142,139,1,0,0,0,142,140,1,
        0,0,0,142,141,1,0,0,0,143,15,1,0,0,0,144,145,5,46,0,0,145,146,5,
        33,0,0,146,148,3,24,12,0,147,149,3,22,11,0,148,147,1,0,0,0,148,149,
        1,0,0,0,149,153,1,0,0,0,150,152,3,26,13,0,151,150,1,0,0,0,152,155,
        1,0,0,0,153,151,1,0,0,0,153,154,1,0,0,0,154,157,1,0,0,0,155,153,
        1,0,0,0,156,158,5,36,0,0,157,156,1,0,0,0,157,158,1,0,0,0,158,17,
        1,0,0,0,159,160,5,19,0,0,160,162,5,46,0,0,161,163,5,36,0,0,162,161,
        1,0,0,0,162,163,1,0,0,0,163,19,1,0,0,0,164,165,5,46,0,0,165,166,
        3,12,6,0,166,21,1,0,0,0,167,168,5,28,0,0,168,169,3,68,34,0,169,23,
        1,0,0,0,170,174,5,46,0,0,171,172,5,37,0,0,172,173,5,45,0,0,173,175,
        5,38,0,0,174,171,1,0,0,0,174,175,1,0,0,0,175,178,1,0,0,0,176,177,
        5,41,0,0,177,179,5,42,0,0,178,176,1,0,0,0,178,179,1,0,0,0,179,25,
        1,0,0,0,180,198,5,12,0,0,181,198,5,13,0,0,182,198,5,14,0,0,183,198,
        5,15,0,0,184,198,5,16,0,0,185,186,5,17,0,0,186,198,3,66,33,0,187,
        188,5,3,0,0,188,190,3,32,16,0,189,191,3,30,15,0,190,189,1,0,0,0,
        190,191,1,0,0,0,191,198,1,0,0,0,192,193,5,21,0,0,193,195,3,32,16,
        0,194,196,3,30,15,0,195,194,1,0,0,0,195,196,1,0,0,0,196,198,1,0,
        0,0,197,180,1,0,0,0,197,181,1,0,0,0,197,182,1,0,0,0,197,183,1,0,
        0,0,197,184,1,0,0,0,197,185,1,0,0,0,197,187,1,0,0,0,197,192,1,0,
        0,0,198,27,1,0,0,0,199,201,5,3,0,0,200,199,1,0,0,0,200,201,1,0,0,
        0,201,202,1,0,0,0,202,203,3,32,16,0,203,204,5,21,0,0,204,206,3,32,
        16,0,205,207,3,30,15,0,206,205,1,0,0,0,206,207,1,0,0,0,207,209,1,
        0,0,0,208,210,5,36,0,0,209,208,1,0,0,0,209,210,1,0,0,0,210,29,1,
        0,0,0,211,212,5,41,0,0,212,213,3,58,29,0,213,214,5,42,0,0,214,31,
        1,0,0,0,215,216,5,46,0,0,216,217,5,35,0,0,217,218,5,46,0,0,218,33,
        1,0,0,0,219,220,5,4,0,0,220,221,5,46,0,0,221,225,5,39,0,0,222,224,
        5,46,0,0,223,222,1,0,0,0,224,227,1,0,0,0,225,223,1,0,0,0,225,226,
        1,0,0,0,226,228,1,0,0,0,227,225,1,0,0,0,228,229,5,40,0,0,229,35,
        1,0,0,0,230,231,5,5,0,0,231,232,5,46,0,0,232,233,5,6,0,0,233,234,
        5,46,0,0,234,238,5,39,0,0,235,237,3,38,19,0,236,235,1,0,0,0,237,
        240,1,0,0,0,238,236,1,0,0,0,238,239,1,0,0,0,239,241,1,0,0,0,240,
        238,1,0,0,0,241,242,5,40,0,0,242,37,1,0,0,0,243,267,3,40,20,0,244,
        261,5,46,0,0,245,246,5,33,0,0,246,251,5,46,0,0,247,248,5,34,0,0,
        248,250,5,46,0,0,249,247,1,0,0,0,250,253,1,0,0,0,251,249,1,0,0,0,
        251,252,1,0,0,0,252,262,1,0,0,0,253,251,1,0,0,0,254,255,5,34,0,0,
        255,257,5,46,0,0,256,254,1,0,0,0,257,260,1,0,0,0,258,256,1,0,0,0,
        258,259,1,0,0,0,259,262,1,0,0,0,260,258,1,0,0,0,261,245,1,0,0,0,
        261,258,1,0,0,0,262,264,1,0,0,0,263,265,5,36,0,0,264,263,1,0,0,0,
        264,265,1,0,0,0,265,267,1,0,0,0,266,243,1,0,0,0,266,244,1,0,0,0,
        267,39,1,0,0,0,268,269,5,20,0,0,269,270,5,46,0,0,270,271,5,46,0,
        0,271,272,5,45,0,0,272,273,5,45,0,0,273,274,5,45,0,0,274,276,5,45,
        0,0,275,277,5,36,0,0,276,275,1,0,0,0,276,277,1,0,0,0,277,41,1,0,
        0,0,278,279,5,7,0,0,279,280,5,46,0,0,280,284,5,39,0,0,281,283,3,
        44,22,0,282,281,1,0,0,0,283,286,1,0,0,0,284,282,1,0,0,0,284,285,
        1,0,0,0,285,287,1,0,0,0,286,284,1,0,0,0,287,288,5,40,0,0,288,43,
        1,0,0,0,289,290,5,46,0,0,290,291,5,21,0,0,291,293,5,46,0,0,292,294,
        5,36,0,0,293,292,1,0,0,0,293,294,1,0,0,0,294,45,1,0,0,0,295,296,
        5,8,0,0,296,297,5,46,0,0,297,301,5,39,0,0,298,300,3,48,24,0,299,
        298,1,0,0,0,300,303,1,0,0,0,301,299,1,0,0,0,301,302,1,0,0,0,302,
        304,1,0,0,0,303,301,1,0,0,0,304,305,5,40,0,0,305,47,1,0,0,0,306,
        307,5,46,0,0,307,308,5,33,0,0,308,313,5,46,0,0,309,310,5,34,0,0,
        310,312,5,46,0,0,311,309,1,0,0,0,312,315,1,0,0,0,313,311,1,0,0,0,
        313,314,1,0,0,0,314,317,1,0,0,0,315,313,1,0,0,0,316,318,5,36,0,0,
        317,316,1,0,0,0,317,318,1,0,0,0,318,49,1,0,0,0,319,320,5,9,0,0,320,
        321,5,46,0,0,321,322,5,6,0,0,322,323,5,46,0,0,323,327,5,39,0,0,324,
        326,3,60,30,0,325,324,1,0,0,0,326,329,1,0,0,0,327,325,1,0,0,0,327,
        328,1,0,0,0,328,330,1,0,0,0,329,327,1,0,0,0,330,331,5,40,0,0,331,
        51,1,0,0,0,332,333,5,10,0,0,333,334,5,46,0,0,334,338,5,39,0,0,335,
        337,3,56,28,0,336,335,1,0,0,0,337,340,1,0,0,0,338,336,1,0,0,0,338,
        339,1,0,0,0,339,341,1,0,0,0,340,338,1,0,0,0,341,342,5,40,0,0,342,
        53,1,0,0,0,343,344,5,11,0,0,344,345,5,46,0,0,345,349,5,39,0,0,346,
        348,3,56,28,0,347,346,1,0,0,0,348,351,1,0,0,0,349,347,1,0,0,0,349,
        350,1,0,0,0,350,352,1,0,0,0,351,349,1,0,0,0,352,353,5,40,0,0,353,
        55,1,0,0,0,354,355,5,46,0,0,355,356,5,33,0,0,356,361,3,58,29,0,357,
        358,5,34,0,0,358,360,3,58,29,0,359,357,1,0,0,0,360,363,1,0,0,0,361,
        359,1,0,0,0,361,362,1,0,0,0,362,365,1,0,0,0,363,361,1,0,0,0,364,
        366,5,36,0,0,365,364,1,0,0,0,365,366,1,0,0,0,366,57,1,0,0,0,367,
        372,3,66,33,0,368,369,7,1,0,0,369,371,3,66,33,0,370,368,1,0,0,0,
        371,374,1,0,0,0,372,370,1,0,0,0,372,373,1,0,0,0,373,59,1,0,0,0,374,
        372,1,0,0,0,375,376,5,46,0,0,376,378,5,13,0,0,377,379,5,47,0,0,378,
        377,1,0,0,0,378,379,1,0,0,0,379,381,1,0,0,0,380,382,5,36,0,0,381,
        380,1,0,0,0,381,382,1,0,0,0,382,394,1,0,0,0,383,384,5,46,0,0,384,
        385,3,64,32,0,385,388,3,62,31,0,386,387,5,21,0,0,387,389,5,46,0,
        0,388,386,1,0,0,0,388,389,1,0,0,0,389,391,1,0,0,0,390,392,5,36,0,
        0,391,390,1,0,0,0,391,392,1,0,0,0,392,394,1,0,0,0,393,375,1,0,0,
        0,393,383,1,0,0,0,394,61,1,0,0,0,395,400,3,66,33,0,396,397,5,34,
        0,0,397,399,3,66,33,0,398,396,1,0,0,0,399,402,1,0,0,0,400,398,1,
        0,0,0,400,401,1,0,0,0,401,63,1,0,0,0,402,400,1,0,0,0,403,404,7,2,
        0,0,404,65,1,0,0,0,405,406,7,3,0,0,406,67,1,0,0,0,407,413,3,70,35,
        0,408,409,3,72,36,0,409,410,3,70,35,0,410,412,1,0,0,0,411,408,1,
        0,0,0,412,415,1,0,0,0,413,411,1,0,0,0,413,414,1,0,0,0,414,69,1,0,
        0,0,415,413,1,0,0,0,416,423,3,32,16,0,417,423,3,66,33,0,418,419,
        5,37,0,0,419,420,3,68,34,0,420,421,5,38,0,0,421,423,1,0,0,0,422,
        416,1,0,0,0,422,417,1,0,0,0,422,418,1,0,0,0,423,71,1,0,0,0,424,425,
        7,4,0,0,425,73,1,0,0,0,49,75,80,87,90,96,108,112,124,134,142,148,
        153,157,162,174,178,190,195,197,200,206,209,225,238,251,258,261,
        264,266,276,284,293,301,313,317,327,338,349,361,365,372,378,381,
        388,391,393,400,413,422
    ]

class appgenParser ( Parser ):

    grammarFileName = "appgen.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'app'", "'table'", "'ref'", "'enum'", 
                     "'view'", "'for'", "'flow'", "'role'", "'rule'", "'llm'", 
                     "'agent'", "'pk'", "'required'", "'unique'", "'hidden'", 
                     "'search'", "'default'", "'in'", "'...'", "'@'", "'->'", 
                     "'=='", "'!='", "'>='", "'<='", "'>'", "'<'", "'='", 
                     "'+'", "'-'", "'*'", "'/'", "':'", "','", "'.'", "';'", 
                     "'('", "')'", "'{'", "'}'", "'['", "']'" ]

    symbolicNames = [ "<INVALID>", "APP", "TABLE", "REF", "ENUM", "VIEW", 
                      "FOR", "FLOW", "ROLE", "RULE", "LLM", "AGENT", "PK", 
                      "REQUIRED", "UNIQUE", "HIDE", "SEARCH", "DEFAULT", 
                      "IN", "ELLIPSIS", "AT", "ARROW", "EQEQ", "NEQ", "GTE", 
                      "LTE", "GT", "LT", "EQ", "PLUS", "MINUS", "STAR", 
                      "SLASH", "COLON", "COMMA", "DOT", "SEMI", "LPAREN", 
                      "RPAREN", "LBRACE", "RBRACE", "LBRACK", "RBRACK", 
                      "BOOL", "DECIMAL", "INT", "IDENT", "STRING", "LINE_COMMENT", 
                      "BLOCK_COMMENT", "WS" ]

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
    RULE_agenticOption = 28
    RULE_agenticValue = 29
    RULE_ruleItem = 30
    RULE_ruleValue = 31
    RULE_ruleOperator = 32
    RULE_literal = 33
    RULE_expression = 34
    RULE_expressionAtom = 35
    RULE_operator = 36

    ruleNames =  [ "schema", "appDecl", "appBlock", "appOption", "element", 
                   "tableDecl", "tableBody", "tableItem", "fieldDecl", "spreadDecl", 
                   "groupDecl", "derivedExpr", "typeRef", "modifier", "relationDecl", 
                   "relationCardinality", "target", "enumDecl", "viewDecl", 
                   "viewItem", "componentPlacement", "flowDecl", "flowStep", 
                   "roleDecl", "permission", "ruleDecl", "llmDecl", "agentDecl", 
                   "agenticOption", "agenticValue", "ruleItem", "ruleValue", 
                   "ruleOperator", "literal", "expression", "expressionAtom", 
                   "operator" ]

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
    LLM=10
    AGENT=11
    PK=12
    REQUIRED=13
    UNIQUE=14
    HIDE=15
    SEARCH=16
    DEFAULT=17
    IN=18
    ELLIPSIS=19
    AT=20
    ARROW=21
    EQEQ=22
    NEQ=23
    GTE=24
    LTE=25
    GT=26
    LT=27
    EQ=28
    PLUS=29
    MINUS=30
    STAR=31
    SLASH=32
    COLON=33
    COMMA=34
    DOT=35
    SEMI=36
    LPAREN=37
    RPAREN=38
    LBRACE=39
    RBRACE=40
    LBRACK=41
    RBRACK=42
    BOOL=43
    DECIMAL=44
    INT=45
    IDENT=46
    STRING=47
    LINE_COMMENT=48
    BLOCK_COMMENT=49
    WS=50

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
            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 74
                self.appDecl()


            self.state = 80
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 70368744181692) != 0):
                self.state = 77
                self.element()
                self.state = 82
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 83
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
            self.state = 85
            self.match(appgenParser.APP)
            self.state = 87
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 86
                _la = self._input.LA(1)
                if not(_la==46 or _la==47):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 89
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
            self.state = 92
            self.match(appgenParser.LBRACE)
            self.state = 96
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 93
                self.appOption()
                self.state = 98
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 99
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
            self.state = 101
            self.match(appgenParser.IDENT)
            self.state = 102
            self.match(appgenParser.COLON)
            self.state = 103
            self.literal()
            self.state = 108
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 104
                self.match(appgenParser.COMMA)
                self.state = 105
                self.literal()
                self.state = 110
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 112
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 111
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
            self.state = 124
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 114
                self.tableDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 115
                self.groupDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 116
                self.enumDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 117
                self.relationDecl()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 118
                self.viewDecl()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 119
                self.flowDecl()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 120
                self.roleDecl()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 121
                self.ruleDecl()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 122
                self.llmDecl()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 123
                self.agentDecl()
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
            self.state = 126
            self.match(appgenParser.TABLE)
            self.state = 127
            self.match(appgenParser.IDENT)
            self.state = 128
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
            self.state = 130
            self.match(appgenParser.LBRACE)
            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 70368744701960) != 0):
                self.state = 131
                self.tableItem()
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 137
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
            self.state = 142
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 139
                self.fieldDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 140
                self.spreadDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 141
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
            self.state = 144
            self.match(appgenParser.IDENT)
            self.state = 145
            self.match(appgenParser.COLON)
            self.state = 146
            self.typeRef()
            self.state = 148
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==28:
                self.state = 147
                self.derivedExpr()


            self.state = 153
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 150
                    self.modifier() 
                self.state = 155
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

            self.state = 157
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 156
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
            self.state = 159
            self.match(appgenParser.ELLIPSIS)
            self.state = 160
            self.match(appgenParser.IDENT)
            self.state = 162
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 161
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
            self.state = 164
            self.match(appgenParser.IDENT)
            self.state = 165
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
            self.state = 167
            self.match(appgenParser.EQ)
            self.state = 168
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
            self.state = 170
            self.match(appgenParser.IDENT)
            self.state = 174
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 171
                self.match(appgenParser.LPAREN)
                self.state = 172
                self.match(appgenParser.INT)
                self.state = 173
                self.match(appgenParser.RPAREN)


            self.state = 178
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 176
                self.match(appgenParser.LBRACK)
                self.state = 177
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
            self.state = 197
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 180
                self.match(appgenParser.PK)
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 2)
                self.state = 181
                self.match(appgenParser.REQUIRED)
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 3)
                self.state = 182
                self.match(appgenParser.UNIQUE)
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 4)
                self.state = 183
                self.match(appgenParser.HIDE)
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 5)
                self.state = 184
                self.match(appgenParser.SEARCH)
                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 6)
                self.state = 185
                self.match(appgenParser.DEFAULT)
                self.state = 186
                self.literal()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 7)
                self.state = 187
                self.match(appgenParser.REF)
                self.state = 188
                self.target()
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==41:
                    self.state = 189
                    self.relationCardinality()


                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 8)
                self.state = 192
                self.match(appgenParser.ARROW)
                self.state = 193
                self.target()
                self.state = 195
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==41:
                    self.state = 194
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
            self.state = 200
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 199
                self.match(appgenParser.REF)


            self.state = 202
            self.target()
            self.state = 203
            self.match(appgenParser.ARROW)
            self.state = 204
            self.target()
            self.state = 206
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==41:
                self.state = 205
                self.relationCardinality()


            self.state = 209
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 208
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
            self.state = 211
            self.match(appgenParser.LBRACK)
            self.state = 212
            self.agenticValue()
            self.state = 213
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
            self.state = 215
            self.match(appgenParser.IDENT)
            self.state = 216
            self.match(appgenParser.DOT)
            self.state = 217
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
            self.state = 219
            self.match(appgenParser.ENUM)
            self.state = 220
            self.match(appgenParser.IDENT)
            self.state = 221
            self.match(appgenParser.LBRACE)
            self.state = 225
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 222
                self.match(appgenParser.IDENT)
                self.state = 227
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 228
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
            self.state = 230
            self.match(appgenParser.VIEW)
            self.state = 231
            self.match(appgenParser.IDENT)
            self.state = 232
            self.match(appgenParser.FOR)
            self.state = 233
            self.match(appgenParser.IDENT)
            self.state = 234
            self.match(appgenParser.LBRACE)
            self.state = 238
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20 or _la==46:
                self.state = 235
                self.viewItem()
                self.state = 240
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 241
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
            self.state = 266
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                self.enterOuterAlt(localctx, 1)
                self.state = 243
                self.componentPlacement()
                pass
            elif token in [46]:
                self.enterOuterAlt(localctx, 2)
                self.state = 244
                self.match(appgenParser.IDENT)
                self.state = 261
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [33]:
                    self.state = 245
                    self.match(appgenParser.COLON)
                    self.state = 246
                    self.match(appgenParser.IDENT)
                    self.state = 251
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==34:
                        self.state = 247
                        self.match(appgenParser.COMMA)
                        self.state = 248
                        self.match(appgenParser.IDENT)
                        self.state = 253
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                elif token in [20, 34, 36, 40, 46]:
                    self.state = 258
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==34:
                        self.state = 254
                        self.match(appgenParser.COMMA)
                        self.state = 255
                        self.match(appgenParser.IDENT)
                        self.state = 260
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 264
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==36:
                    self.state = 263
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
            self.state = 268
            self.match(appgenParser.AT)
            self.state = 269
            self.match(appgenParser.IDENT)
            self.state = 270
            self.match(appgenParser.IDENT)
            self.state = 271
            self.match(appgenParser.INT)
            self.state = 272
            self.match(appgenParser.INT)
            self.state = 273
            self.match(appgenParser.INT)
            self.state = 274
            self.match(appgenParser.INT)
            self.state = 276
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 275
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
            self.state = 278
            self.match(appgenParser.FLOW)
            self.state = 279
            self.match(appgenParser.IDENT)
            self.state = 280
            self.match(appgenParser.LBRACE)
            self.state = 284
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 281
                self.flowStep()
                self.state = 286
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 287
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
            self.state = 289
            self.match(appgenParser.IDENT)
            self.state = 290
            self.match(appgenParser.ARROW)
            self.state = 291
            self.match(appgenParser.IDENT)
            self.state = 293
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 292
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
            self.state = 295
            self.match(appgenParser.ROLE)
            self.state = 296
            self.match(appgenParser.IDENT)
            self.state = 297
            self.match(appgenParser.LBRACE)
            self.state = 301
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 298
                self.permission()
                self.state = 303
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 304
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
            self.state = 306
            self.match(appgenParser.IDENT)
            self.state = 307
            self.match(appgenParser.COLON)
            self.state = 308
            self.match(appgenParser.IDENT)
            self.state = 313
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 309
                self.match(appgenParser.COMMA)
                self.state = 310
                self.match(appgenParser.IDENT)
                self.state = 315
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 317
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 316
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
            self.state = 319
            self.match(appgenParser.RULE)
            self.state = 320
            self.match(appgenParser.IDENT)
            self.state = 321
            self.match(appgenParser.FOR)
            self.state = 322
            self.match(appgenParser.IDENT)
            self.state = 323
            self.match(appgenParser.LBRACE)
            self.state = 327
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 324
                self.ruleItem()
                self.state = 329
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 330
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
            self.state = 332
            self.match(appgenParser.LLM)
            self.state = 333
            self.match(appgenParser.IDENT)
            self.state = 334
            self.match(appgenParser.LBRACE)
            self.state = 338
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 335
                self.agenticOption()
                self.state = 340
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 341
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
            self.state = 343
            self.match(appgenParser.AGENT)
            self.state = 344
            self.match(appgenParser.IDENT)
            self.state = 345
            self.match(appgenParser.LBRACE)
            self.state = 349
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==46:
                self.state = 346
                self.agenticOption()
                self.state = 351
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 352
            self.match(appgenParser.RBRACE)
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
        self.enterRule(localctx, 56, self.RULE_agenticOption)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 354
            self.match(appgenParser.IDENT)
            self.state = 355
            self.match(appgenParser.COLON)
            self.state = 356
            self.agenticValue()
            self.state = 361
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 357
                self.match(appgenParser.COMMA)
                self.state = 358
                self.agenticValue()
                self.state = 363
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 365
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 364
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
        self.enterRule(localctx, 58, self.RULE_agenticValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 367
            self.literal()
            self.state = 372
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30 or _la==35:
                self.state = 368
                _la = self._input.LA(1)
                if not(_la==30 or _la==35):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 369
                self.literal()
                self.state = 374
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
        self.enterRule(localctx, 60, self.RULE_ruleItem)
        self._la = 0 # Token type
        try:
            self.state = 393
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,45,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 375
                self.match(appgenParser.IDENT)
                self.state = 376
                self.match(appgenParser.REQUIRED)
                self.state = 378
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==47:
                    self.state = 377
                    self.match(appgenParser.STRING)


                self.state = 381
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==36:
                    self.state = 380
                    self.match(appgenParser.SEMI)


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 383
                self.match(appgenParser.IDENT)
                self.state = 384
                self.ruleOperator()
                self.state = 385
                self.ruleValue()
                self.state = 388
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==21:
                    self.state = 386
                    self.match(appgenParser.ARROW)
                    self.state = 387
                    self.match(appgenParser.IDENT)


                self.state = 391
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==36:
                    self.state = 390
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
        self.enterRule(localctx, 62, self.RULE_ruleValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 395
            self.literal()
            self.state = 400
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 396
                self.match(appgenParser.COMMA)
                self.state = 397
                self.literal()
                self.state = 402
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
        self.enterRule(localctx, 64, self.RULE_ruleOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 403
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 264503296) != 0)):
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
        self.enterRule(localctx, 66, self.RULE_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 405
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 272678883688448) != 0)):
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
        self.enterRule(localctx, 68, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 407
            self.expressionAtom()
            self.state = 413
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8053063680) != 0):
                self.state = 408
                self.operator()
                self.state = 409
                self.expressionAtom()
                self.state = 415
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
        self.enterRule(localctx, 70, self.RULE_expressionAtom)
        try:
            self.state = 422
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,48,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 416
                self.target()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 417
                self.literal()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 418
                self.match(appgenParser.LPAREN)
                self.state = 419
                self.expression()
                self.state = 420
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
        self.enterRule(localctx, 72, self.RULE_operator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 424
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8053063680) != 0)):
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





