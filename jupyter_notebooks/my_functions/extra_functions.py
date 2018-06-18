import pandas as pd

"""  Used with a mapping fuction to create a locale column on a DataFrame  """
locale_map = {11: 'City', 12: 'City', 13: 'City', 14: 'City',
              21: 'Suburban', 22: 'Suburban', 23: 'Suburban', 24: 'Suburban',
              31: 'Town', 32: 'Town', 33: 'Town', 34: 'Town',
              41: 'Rural', 42: 'Rural', 43: 'Rural', 44: 'Rural'}

def students_in_11_or_12(g11, g12):
    """Inputs 11th and 12th grade enrollment flags from the CRDC dataset
        Returns a label representing whether or not a school has students in 11th or 12th grade
        """
    if g11 == 'Yes':
        return 'Yes'
    if g12 == 'Yes':
        return 'Yes'
    return 'No'

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

def de_ap_enrollments(de_only, ap_only, neither, both, groupby_field=False):
    """ Takes in four DataFrames (de_only, ap_only, neither, and both) and
        breaks their high-school (calculated by the hs_enrollment averager function) enrollments
        down by a specific field (if specified) """

    if groupby_field != False:
        de_only_field = de_only.groupby(groupby_field)['hs_total_enrollment'].sum().rename('DE_Only_hs_students')
        ap_only_field = ap_only.groupby(groupby_field)['hs_total_enrollment'].sum().rename('AP_Only_hs_students')
        neither_AP_DE_field = neither.groupby(groupby_field)['hs_total_enrollment'].sum().rename('Neither_AP_DE_hs_students')
        both_AP_DE_field = both.groupby(groupby_field)['hs_total_enrollment'].sum().rename('Both_AP_DE_hs_students')

        combined = pd.concat([de_only_field, ap_only_field,
                              neither_AP_DE_field, both_AP_DE_field], axis = 1).fillna(0).astype(int)

        combined['Total'] = combined['DE_Only_hs_students'] + combined['AP_Only_hs_students'] \
                            + combined['Neither_AP_DE_hs_students'] + combined['Both_AP_DE_hs_students']

        combined['DE_Only %'] = round(combined['DE_Only_hs_students'] / combined['Total'] * 100, 1)
        combined['AP_Only %'] = round(combined['AP_Only_hs_students'] / combined['Total'] * 100, 1)
        combined['Neither_AP_DE %'] = round(combined['Neither_AP_DE_hs_students'] / combined['Total'] * 100, 1)
        combined['Both_AP_DE %'] = round(combined['Both_AP_DE_hs_students'] / combined['Total'] * 100, 1)

        order = ['DE_Only_hs_students', 'DE_Only %', 'AP_Only_hs_students', 'AP_Only %',
                 'Neither_AP_DE_hs_students', 'Neither_AP_DE %', 'Both_AP_DE_hs_students', 'Both_AP_DE %', 'Total']

        return combined[order]
    else:
        de_only_field = de_only['hs_total_enrollment'].sum()#.rename('DE_Only_hs_students')
        ap_only_field = ap_only['hs_total_enrollment'].sum()#.rename('AP_Only_hs_students')
        neither_AP_DE_field = neither['hs_total_enrollment'].sum()#.rename('Neither_AP_DE_hs_students')
        both_AP_DE_field = both['hs_total_enrollment'].sum()#.rename('Both_AP_DE_hs_students')

        combined = pd.DataFrame({'DE_Only_hs_students': de_only_field,
                                 'AP_Only_hs_students': ap_only_field,
                                 'Neither_AP_DE_hs_students': neither_AP_DE_field,
                                 'Both_AP_DE_hs_students': both_AP_DE_field},
                               index = ['HS Enrollments'])

        combined['Total'] = combined['DE_Only_hs_students'] + combined['AP_Only_hs_students'] \
                            + combined['Neither_AP_DE_hs_students'] + combined['Both_AP_DE_hs_students']

        combined['DE_Only %'] = round(combined['DE_Only_hs_students'] / combined['Total'] * 100, 1)
        combined['AP_Only %'] = round(combined['AP_Only_hs_students'] / combined['Total'] * 100, 1)
        combined['Neither_AP_DE %'] = round(combined['Neither_AP_DE_hs_students'] / combined['Total'] * 100, 1)
        combined['Both_AP_DE %'] = round(combined['Both_AP_DE_hs_students'] / combined['Total'] * 100, 1)

        order = ['DE_Only_hs_students', 'DE_Only %', 'AP_Only_hs_students', 'AP_Only %',
                 'Neither_AP_DE_hs_students', 'Neither_AP_DE %', 'Both_AP_DE_hs_students', 'Both_AP_DE %', 'Total']

        return combined[order]

def add_de_ap_pcts(df_input):
    """ Adds a percentage breakdown of all the columns (DE_Only, AP_Only, etc.) in the inputted DataFrame (df) """
    df = df_input.copy()
    df['DE_Only %'] = round(df['DE_Only'] / df['Total'] * 100, 1)
    df['AP_Only %'] = round(df['AP_Only'] / df['Total'] * 100, 1)
    df['Neither_AP_DE %'] = round(df['Neither_AP_DE'] / df['Total'] * 100, 1)
    df['Both_AP_DE %'] = round(df['Both_AP_DE'] / df['Total'] * 100, 1)

    order = ['DE_Only', 'DE_Only %', 'AP_Only', 'AP_Only %',
             'Neither_AP_DE', 'Neither_AP_DE %', 'Both_AP_DE', 'Both_AP_DE %', 'Total']

    return df[order]

def flag_grouper(dataset, groupby_col, ap_or_de, keep_index=False):
    """ inputs: dataset (pandas.DataFrame), groupby_col (column name that
            should be grouped on), ap_or_de ('AP' for AP Stats, 'DE' for DE Stats),
            keep_index (retain the native index if set to True).

        returns:  DataFrame containing AP/DE Stats for the groupby_col"""
    if ap_or_de == 'DE':
        second_group = 'SCH_DUAL_IND'
    elif ap_or_de == 'AP':
        second_group = 'SCH_APENR_IND'
    else:
        print('Error in ap_or_de term.')
        return

    flag_group = dataset.groupby([groupby_col, second_group])['LEAID'].count().unstack().reset_index()

    flag_group['# of HS Schools'] = (flag_group['Yes'] + flag_group['No'])
    flag_group[ap_or_de + ' Offering Rate'] = round(flag_group['Yes'] / (flag_group['Yes'] + flag_group['No']) * 100, 1)
    flag_group = flag_group.rename({'Yes': '# of ' + ap_or_de +  ' Schools'}, axis=1)
    flag_group = flag_group.drop(['No'], axis = 1)

    order = [groupby_col, '# of HS Schools', '# of ' + ap_or_de +  ' Schools', ap_or_de + ' Offering Rate']

    if keep_index:
        return flag_group[order]
    return flag_group[order[1:]]

def missing_value_mapper(value):
    """Converts any negative number into 0, as these negative numbers represent missing/null values"""
    if isinstance(value, int):
        if value < 0:
            return 0
    return value

def school_grade_range(df):
    """Calculates the number of schools in a given DataFrame (df) of a particular distribution of grades:
        Example:  If a school (in df) offers grades 9,10,11,12 exclusively, they are placed in the '9-12'
                    category. """
    df_grade_range = []
    for index, row in df.iterrows():
        grade_range = []

        if row.SCH_GRADE_G12 == 'Yes':
            grade_range.append(12)
        if row.SCH_GRADE_G11 == 'Yes':
            grade_range.append(11)
        if row.SCH_GRADE_G10 == 'Yes':
            grade_range.append(10)
        if row.SCH_GRADE_G09 == 'Yes':
            grade_range.append(9)
        if row.SCH_GRADE_G08 == 'Yes':
            grade_range.append(8)
        if row.SCH_GRADE_G07 == 'Yes':
            grade_range.append(7)
        if row.SCH_GRADE_G06 == 'Yes':
            grade_range.append(6)
        if row.SCH_GRADE_G05 == 'Yes':
            grade_range.append(5)
        if row.SCH_GRADE_G04 == 'Yes':
            grade_range.append(4)
        if row.SCH_GRADE_G03 == 'Yes':
            grade_range.append(3)
        if row.SCH_GRADE_G02 == 'Yes':
            grade_range.append(2)
        if row.SCH_GRADE_G01 == 'Yes':
            grade_range.append(1)
        if row.SCH_GRADE_KG == 'Yes':
            grade_range.append('kg')
        if row.SCH_GRADE_PS == 'Yes':
            grade_range.append('pk')

        if grade_range == [12,11,10,9,8,7,6,5,4,3,2,1,'kg','pk']:
            df_grade_range.append('pk-12')
        elif grade_range == [12,11,10,9,8,7,6,5,4,3,2,1,'kg']:
            df_grade_range.append('kg-12')
        elif grade_range == [12,11,10,9,8,7,6,5]:
            df_grade_range.append('05-12')
        elif grade_range == [12,11,10,9,8,7,6]:
            df_grade_range.append('06-12')
        elif grade_range == [12,11,10,9,8,7]:
            df_grade_range.append('07-12')
        elif grade_range == [12,11,10,9,8]:
            df_grade_range.append('08-12')
        elif grade_range == [12,11,10,9]:
            df_grade_range.append('09-12')
        elif grade_range == [11,10,9]:
            df_grade_range.append('09-11')
        elif grade_range == [10,9]:
            df_grade_range.append('09-10')
        elif grade_range == [12,11,10]:
            df_grade_range.append('10-12')
        elif grade_range == [12,11]:
            df_grade_range.append('11-12')
        elif grade_range == [9]:
            df_grade_range.append('9-only')
        elif grade_range == [10]:
            df_grade_range.append('10-only')
        elif grade_range == [11]:
            df_grade_range.append('11-only')
        elif grade_range == [12]:
            df_grade_range.append('12-only')
        else:
            df_grade_range.append('other')
    return pd.DataFrame(df_grade_range, columns=['grade_range'])

def have_gr9_or_younger(df):
    """Calculates the number of schools in a given DataFrame (df) offer grades of 8th or younger (i.e. non-high school grades)"""
    count = 0
    for index, row in df.iterrows():
        if row.SCH_GRADE_G08 == 'Yes':
            count += 1
        elif row.SCH_GRADE_G07 == 'Yes':
            count += 1
        elif row.SCH_GRADE_G06 == 'Yes':
            count += 1
        elif row.SCH_GRADE_G05 == 'Yes':
            count += 1
        elif row.SCH_GRADE_G04 == 'Yes':
            count += 1
        elif row.SCH_GRADE_G03 == 'Yes':
            count += 1
        elif row.SCH_GRADE_G02 == 'Yes':
            count += 1
        elif row.SCH_GRADE_G01 == 'Yes':
            count += 1
        elif row.SCH_GRADE_KG == 'Yes':
            count += 1
        elif row.SCH_GRADE_PS == 'Yes':
            count += 1
    return round(count / len(df),3)
