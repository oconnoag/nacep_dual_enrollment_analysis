def hs_enrollment_averager(df):
    """Provides a work-around for figuring out the number of high school students in a school that offers grades 8th
        or lower.  Scales the total enrollment of each school by the ratio of high school grades offered : total grades
        offered

        Takes in a DataFrame and returns a list of 'averaged' enrollments for each school."""
    hs_enrollment_list = []
    for index, row in df.iterrows():
        all_count = 0
        hs_count = 0
        if row.SCH_GRADE_G12 == 'Yes':
            hs_count += 1
            all_count += 1
        if row.SCH_GRADE_G11 == 'Yes':
            hs_count += 1
            all_count += 1
        if row.SCH_GRADE_G10 == 'Yes':
            hs_count += 1
            all_count += 1
        if row.SCH_GRADE_G09 == 'Yes':
            hs_count += 1
            all_count += 1

        if row.SCH_GRADE_G08 == 'Yes':
            all_count += 1
        if row.SCH_GRADE_G07 == 'Yes':
            all_count += 1
        if row.SCH_GRADE_G06 == 'Yes':
            all_count += 1
        if row.SCH_GRADE_G05 == 'Yes':
            all_count += 1
        if row.SCH_GRADE_G04 == 'Yes':
            all_count += 1
        if row.SCH_GRADE_G03 == 'Yes':
            all_count += 1
        if row.SCH_GRADE_G02 == 'Yes':
            all_count += 1
        if row.SCH_GRADE_G01 == 'Yes':
            all_count += 1
        if row.SCH_GRADE_KG == 'Yes':
            all_count += 1
        if row.SCH_GRADE_PS == 'Yes':
            all_count += 1

        if all_count > 0:
            hs_ratio = hs_count / all_count
            hs_enrollment = int(round(row['total_enrollment'] * hs_ratio, 0))
        else:
            hs_enrollment = row['total_enrollment']

        hs_enrollment_list.append(hs_enrollment)
    return hs_enrollment_list

def school_sizer(enroll):
    """ Takes in the total (high school -- see the hs_enrollment_averager
        function) enrollment of a school and returns a number
        that corresponds to the size-group of that school:
            1: <100 students
            2: 100-499 students
            3: 500-1199 students
            4: 1200+ students """
    if enroll < 100:
        return 1
    elif 100 <= enroll < 500:
        return 2
    elif 500 <= enroll < 1200:
        return 3
    return 4

def region_mapper(state):
    """ Takes in the 'state' column from a DataFrame and assigns the
        school to the according region containing that state.

        Uses the Regional Accreditation Categories for the state assignments.
        """

    if state in "NY,NJ,PA,DE,MD,DC".split(','):
        return "MSCHE"
    elif state in "CT,ME,MA,NH,RI,VT".split(','):
        return "NEASC"
    elif state in "AR,AZ,CO,IA,IL,IN,KS,MI,MN,MO,ND,NE,NM,OH,OK,SD,WI,WV,WY".split(','):
        return "HLC"
    elif state in "AK,ID,MT,NV,OR,UT,WA".split(','):
        return "NWCCU"
    elif state in "AL,FL,GA,KY,LA,MS,NC,SC,TN,TX,VA".split(','):
        return "SACS"
    elif state in "CA,HI".split(','):
        return "WASC"
    else:
        return "Messed Up"

def eth_grouper(pct):
    """ Takes in the percent ethnicity of a school and returns a 'Eth Group'
        according to that percent.

        Eth Groups are quintiles:
            1:  0-20%,
            2:  21-40%,
            3:  41-60%,
            4:  61-80%,
            5:  81-100%
        """
    if pct <= .20:
        return 1
    elif .20 < pct <= .4:
        return 2
    elif .4 < pct <= 0.6:
        return 3
    elif .6 < pct <= .8:
        return 4
    return 5
