def define_badges(b):

    # Classes
    b.add("f\0\0\0", None, "STR_CLASS_FLAG")
    b.add("m\0\0\0", None, "STR_CLASS_USAGE")
    b.add("o\0\0\0", None, "STR_CLASS_OPERATOR")
    b.add("p\0\0\0", None, "STR_CLASS_PROPULSION")

    # Modes
    b.add("mPAS", None, "STR_MODE_PAS")
    b.add("mFRE", None, "STR_MODE_FRE")
    b.add("mMIX", None, "STR_MODE_MIX")
    b.add("mEXP", None, "STR_MODE_EXP")
    b.add("mEXF", None, "STR_MODE_EXF")
    b.add("mHEF", None, "STR_MODE_HEF")
