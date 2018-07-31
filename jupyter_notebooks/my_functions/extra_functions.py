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

def missing_value_mapper(value):
    """Used with an applymap() function on an entire DataFrame.
       Converts any negative number into 0, as these negative numbers represent missing/null values"""
    if isinstance(value, int):
        if value < 0:
            return 0
    return value

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

def add_enrollment_columns(df):
    """Used in the Initial Filtration File to sum up the enrollments - Requires functions hs_enrollment_averager and
        missing_value_mapper from the extra_functions module.

        Inputs a DataFrame (df)

        Returns a copy of that DataFrame (df_copy) with the summed DE Enrollment, AP Enrollment, Total Enrollment,
        and High School Enrollment.
    """
    df_copy = df.copy()
    df_copy = df_copy.applymap(missing_value_mapper)
    df_copy['de_total'] = df_copy['TOT_DUALENR_M'] + df_copy['TOT_DUALENR_F']
    df_copy['ap_total'] = df_copy['TOT_APENR_M'] + df_copy['TOT_APENR_F']
    df_copy['total_enrollment'] = df_copy['TOT_ENR_M'] + df_copy['TOT_ENR_F']
    df_copy['hs_total'] = hs_enrollment_averager(df_copy)

    return df_copy

def enrollment_summary(df, phrase):
    """Used in conjunction with the add_enrollment_columns function in the extra_funcitons module to make DataFrames
        containing #Schools, DE Enrollment, AP Enrollment, and HS Enrollment.

        Inputs a DataFrame (df), and String (phrase) that will become the index term for the DataFrame.

        Returns a DataFrame containing the summed enrollment values."""
    df_copy = df.copy()
    num_schools = len(df_copy)
    hs_students = df_copy['hs_total'].sum()
    de_students = df_copy['de_total'].sum()
    ap_students = df_copy['ap_total'].sum()

    return pd.DataFrame({phrase: [num_schools, hs_students, de_students, ap_students]},
                index = ['Number of Schools', 'High Students', 'DE Students', 'AP Students']).T

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

def region_mapper_nacep(state):
    """ Takes in the 'state' column from a DataFrame and assigns the
        school to the according region containing that state.

        Uses the NACEP-defined Categories for the state assignments.
        """

    if state in "NY,NJ,PA,DE,MD,DC,CT,ME,MA,NH,RI,VT,VA".split(','):
        return "1"
    elif state in "MI,IN,OH,WV,KY,TN,NC,SC,AL,MS,GA,FL".split(','):
        return "2"
    elif state in "IL,MO,AR,LA,OK,KS,TX".split(','):
        return "3"
    elif state in "MT,ID,WY,ND,SD,NE,IA,MN,WI".split(','):
        return "4"
    elif state in "OR,WA,CA,NV,UT,AZ,CO,NM,AK,HI".split(','):
        return "5"
    else:
        return "Messed Up"

def region_mapper_census(state):
    """ Takes in the 'state' column from a DataFrame and assigns the
        school to the according region containing that state.

        Uses the census-defined Categories for the state assignments.
        """
    # Northeast
    if state in "CT,ME,MA,NH,RI,VT".split(','):
        return "New England"
    elif state in "NY,PA,NJ,".split(','):
        return "Middle Atlantic"
    # South
    elif state in "DE,MD,DC,VA,WV,NC,SC,GA,FL".split(','):
        return "South Atlantic"
    elif state in "KY,TN,AL,MS".split(','):
        return "East South Central"
    elif state in "AR,LA,OK,TX".split(','):
        return "West South Central"
    # Midwest
    elif state in 'MI,OH,IN,IL,WI'.split(','):
        return 'East North Central'
    elif state in 'MO,IA,MN,ND,SD,NE,KS'.split(','):
        return 'West North Central'
    # West
    elif state in 'MT,ID,WY,CO,UT,AZ,NM,NV'.split(','):
        return 'Mountain'
    elif state in 'WA,OR,CA,HI,AK'.split(','):
        return 'Pacific'

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
        de_only_field = de_only.groupby(groupby_field)['hs_total_enrollment'].sum().rename('HS Students in DE-Only Schools')
        ap_only_field = ap_only.groupby(groupby_field)['hs_total_enrollment'].sum().rename('HS Students in AP-Only Schools')
        neither_AP_DE_field = neither.groupby(groupby_field)['hs_total_enrollment'].sum().rename('HS Students in Schools w/ Neither')
        both_AP_DE_field = both.groupby(groupby_field)['hs_total_enrollment'].sum().rename('HS Students in Schools w/ Both')

        combined = pd.concat([de_only_field, ap_only_field,
                              neither_AP_DE_field, both_AP_DE_field], axis = 1).fillna(0).astype(int)

        combined['Total'] = combined['HS Students in DE-Only Schools'] + combined['HS Students in AP-Only Schools'] \
                            + combined['HS Students in Schools w/ Neither'] + combined['HS Students in Schools w/ Both']

        combined['% DE-Only Schools'] = round(combined['HS Students in DE-Only Schools'] / combined['Total'] * 100, 1)
        combined['% AP-Only Schools'] = round(combined['HS Students in AP-Only Schools'] / combined['Total'] * 100, 1)
        combined['% Neither Schools'] = round(combined['HS Students in Schools w/ Neither'] / combined['Total'] * 100, 1)
        combined['% Both Schools'] = round(combined['HS Students in Schools w/ Both'] / combined['Total'] * 100, 1)

        order = ['HS Students in DE-Only Schools', '% DE-Only Schools', 'HS Students in AP-Only Schools', '% AP-Only Schools',
                 'HS Students in Schools w/ Neither', '% Neither Schools', 'HS Students in Schools w/ Both', '% Both Schools', 'Total']

        return combined[order]
    else:
        de_only_field = de_only['hs_total_enrollment'].sum()#.rename('HS Students in DE-Only Schools')
        ap_only_field = ap_only['hs_total_enrollment'].sum()#.rename('HS Students in DE-Only Schools')
        neither_AP_DE_field = neither['hs_total_enrollment'].sum()#.rename('HS Students in DE-Only Schools')
        both_AP_DE_field = both['hs_total_enrollment'].sum()#.rename('HS Students in Schools w/ Both')

        combined = pd.DataFrame({'HS Students in DE-Only Schools': de_only_field,
                                 'HS Students in AP-Only Schools': ap_only_field,
                                 'HS Students in Schools w/ Neither': neither_AP_DE_field,
                                 'HS Students in Schools w/ Both': both_AP_DE_field},
                               index = ['HS Enrollments'])

        combined['Total'] = combined['HS Students in DE-Only Schools'] + combined['HS Students in AP-Only Schools'] \
                            + combined['HS Students in Schools w/ Neither'] + combined['HS Students in Schools w/ Both']

        combined['% DE-Only Schools'] = round(combined['HS Students in DE-Only Schools'] / combined['Total'] * 100, 1)
        combined['% AP-Only Schools'] = round(combined['HS Students in AP-Only Schools'] / combined['Total'] * 100, 1)
        combined['% Neither Schools'] = round(combined['HS Students in Schools w/ Neither'] / combined['Total'] * 100, 1)
        combined['% Both Schools'] = round(combined['HS Students in Schools w/ Both'] / combined['Total'] * 100, 1)

        order = ['HS Students in DE-Only Schools', '% DE-Only Schools', 'HS Students in AP-Only Schools', '% AP-Only Schools',
                 'HS Students in Schools w/ Neither', '% Neither Schools', 'HS Students in Schools w/ Both', '% Both Schools', 'Total']

        return combined[order]

def add_de_ap_pcts(df_input):
    """ Adds a percentage breakdown of all the columns (DE Only, AP Only, etc.) in the inputted DataFrame (df) """
    df = df_input.copy()
    df['% DE-Only Schools in Group'] = round(df['DE Only'] / df['Total'] * 100, 1)
    df['% AP-Only Schools in Group'] = round(df['AP Only'] / df['Total'] * 100, 1)
    df['% Neither Schools in Group'] = round(df['Neither AP DE'] / df['Total'] * 100, 1)
    df['% Both Schools in Group'] = round(df['Both AP DE'] / df['Total'] * 100, 1)

    order = ['DE Only', '% DE-Only Schools in Group', 'AP Only', '% AP-Only Schools in Group',
             'Neither AP DE', '% Neither Schools in Group', 'Both AP DE', '% Both Schools in Group', 'Total']

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
    flag_group = flag_group.rename({'Yes': '# Schools Offering ' + ap_or_de }, axis=1)
    flag_group = flag_group.drop(['No'], axis = 1)

    order = [groupby_col, '# of HS Schools', '# Schools Offering ' + ap_or_de, ap_or_de + ' Offering Rate']

    if keep_index:
        return flag_group[order]
    return flag_group[order[1:]]

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

def enrollment_compiler(dataset, groupby_col):
    """Used in the Enrollment Analyses Files to create DataFrames with the exact structures (can only be used for
        group attributes of a school (not students -- see the enrollment_compiler_layerer function))

        Inputs a DataFrame (dataset) and a Column in the DataFrame to perform a groupby() (groupby_col)

        Returns a Fully compiled DataFrame"""
    # These are used for calculating Ratios, Gaps, and Participation Rates
    hs_total = dataset['hs_total_enrollment'].sum()
    de_total = dataset['de_total_enrollment'].sum()
    ap_total = dataset['ap_total_enrollment'].sum()
    hs_breakdown_totals = dataset.groupby(groupby_col)['hs_total_enrollment'].sum()

    # Used to substantiate the DataFrame
    hs_total_enrolls = dataset.groupby(groupby_col)['hs_total_enrollment'].sum().rename('HS Students') # Based on the Averager Function
    hs_pcts = round(hs_total_enrolls / hs_total * 100, 1).rename('%Total HS Students')

    de_total_enrolls = dataset.groupby(groupby_col)['de_total_enrollment'].sum().rename('DE Students')
    de_pcts = round(de_total_enrolls / de_total * 100, 1).rename('%Total DE Students')
    de_gap = (de_pcts - hs_pcts).rename('DE Gap')
    de_participation = round(de_total_enrolls / hs_breakdown_totals * 100, 1).rename('DE Participation Rate')

    ap_total_enrolls = dataset.groupby(groupby_col)['ap_total_enrollment'].sum().rename('AP Students')
    ap_pcts = round(ap_total_enrolls / ap_total * 100, 1).rename('%Total AP Students')
    ap_gap = (ap_pcts - hs_pcts).rename('AP Gap')
    ap_participation = round(ap_total_enrolls / hs_breakdown_totals * 100, 1).rename('AP Participation Rate')

    return pd.concat([hs_total_enrolls, hs_pcts, de_total_enrolls, de_pcts, de_gap, de_participation,
                      ap_total_enrolls, ap_pcts, ap_gap, ap_participation], axis = 1)

def enrollment_by_group_compiler(dataset, groupby_col, by_group_abbr):
    """Used in the Enrollment Analyses Files to create DataFrames with the exact structures (can only be used for
        group attributes of a school) -- must provide the correct group abbreviation.

        Example:  For non-whites by state:  groupby_col = 'LEA_STATE', by_group_abbr = 'nonwhite'

        Inputs a DataFrame (dataset), a Column in the DataFrame to perform a groupby() (groupby_col), and the
        abreviation for a group you would like to breakdown numerically.

        Returns a Fully compiled DataFrame"""

    # These are used for calculating Ratios, Gaps, and Participation Rates
    hs_total = dataset['hs_' + by_group_abbr].sum()
    de_total = dataset['de_' + by_group_abbr + '_enrollment'].sum()
    ap_total = dataset['ap_' + by_group_abbr + '_enrollment'].sum()
    hs_breakdown_totals = dataset.groupby(groupby_col)['hs_total_enrollment'].sum()

    # Used to substantiate the DataFrame
    hs_total_enrolls = dataset.groupby(groupby_col)['hs_' + by_group_abbr].sum().rename(by_group_abbr.title() + ' HS Students').astype(int) # Based on the Averager Function
    hs_pcts = round(hs_total_enrolls / hs_total * 100, 1).rename('%Total ' + by_group_abbr.title() + ' HS Students')

    de_total_enrolls = dataset.groupby(groupby_col)['de_' + by_group_abbr + '_enrollment'].sum().rename(by_group_abbr.title() + ' DE Students')
    de_pcts = round(de_total_enrolls / de_total * 100, 1).rename('%Total ' + by_group_abbr.title() + ' DE Students')
    de_gap = (de_pcts - hs_pcts).rename(by_group_abbr + ' DE Gap')
    de_participation = round(de_total_enrolls / hs_breakdown_totals * 100, 1).rename(by_group_abbr.title() + ' DE Participation Rate')

    ap_total_enrolls = dataset.groupby(groupby_col)['ap_' + by_group_abbr + '_enrollment'].sum().rename(by_group_abbr.title() + ' AP Students')
    ap_pcts = round(ap_total_enrolls / ap_total * 100, 1).rename('%Total ' + by_group_abbr.title() + ' AP Students')
    ap_gap = (ap_pcts - hs_pcts).rename(by_group_abbr + ' AP Gap')
    ap_participation = round(ap_total_enrolls / hs_breakdown_totals * 100, 1).rename(by_group_abbr.title() + ' AP Participation Rate')

    return pd.concat([hs_total_enrolls, hs_pcts, de_total_enrolls, de_pcts, de_gap, de_participation,
                      ap_total_enrolls, ap_pcts, ap_gap, ap_participation], axis = 1)

def enrollment_compiler_layerer(dataset, hs_col, de_col, ap_col, row_name):
    """Used in the Enrollment Analyses Files to create DataFrames with the exact structures (can only be used for
        student attributes of a school (not students -- see the enrollment_compiler function)) -- this function
        can only handle one 'row at a time', and the compiled DataFrame needs to be created using the
        pd.Concat() function.

        Inputs a DataFrame (dataset), a High School Enrollment column (hs_col),
            a DE Enrollment column (de_col), an AP Enrollment column (ap_col), and
            the string name of a row that is used for the index (row_name)

        Returns a one-rowed DataFrame"""
    # These are used for calculating Ratios, Gaps, and Participation Rates
    hs_total = dataset['hs_total_enrollment'].sum()
    de_total = dataset['de_total_enrollment'].sum()
    ap_total = dataset['ap_total_enrollment'].sum()

    # Used to substantiate the DataFrame
    hs_total_enrolls = dataset[hs_col].sum() # Based on the Averager Function
    hs_pcts = round(hs_total_enrolls / hs_total * 100, 1)

    de_total_enrolls = dataset[de_col].sum()
    de_pcts = round(de_total_enrolls / de_total * 100, 1)
    de_gap = (de_pcts - hs_pcts)
    de_participation = round(de_total_enrolls / hs_total_enrolls * 100, 1)

    ap_total_enrolls = dataset[ap_col].sum()
    ap_pcts = round(ap_total_enrolls / ap_total * 100, 1)
    ap_gap = (ap_pcts - hs_pcts)
    ap_participation = round(ap_total_enrolls / hs_total_enrolls * 100, 1)

    order = ['HS Students','%Total HS Students', 'DE Students', '%Total DE Students', 'DE Gap','DE Participation Rate',
             'AP Students', '%Total AP Students', 'AP Gap', 'AP Participation Rate']
    return pd.DataFrame({'HS Students': [hs_total_enrolls],
                  '%Total HS Students': [hs_pcts],
                  'DE Students': [de_total_enrolls],
                  '%Total DE Students': [de_pcts],
                  'DE Gap': [de_gap],
                  'DE Participation Rate': [de_participation],
                  'AP Students': [ap_total_enrolls],
                  '%Total AP Students': [ap_pcts],
                  'AP Gap': [ap_gap],
                  'AP Participation Rate': [ap_participation]},
                 index = [row_name])[order]

def by_offering_enrollment_compiler(de_yes, ap_yes, groupby_col):
    """Used in the "By Offering" Enrollment Analyses Files to create DataFrames with the exact structures (can only be used for
        group attributes of a school (not students -- see the enrollment_compiler_layerer function))

        Inputs a DataFrame (dataset) and a Column in the DataFrame to perform a groupby() (groupby_col)

        Returns a Fully compiled DataFrame"""
    # These are used for calculating Ratios, Gaps, and Participation Rates
    deYes_hs_total = de_yes['hs_total_enrollment'].sum()
    apYes_hs_total = ap_yes['hs_total_enrollment'].sum()
    de_total = de_yes['de_total_enrollment'].sum()
    ap_total = ap_yes['ap_total_enrollment'].sum()

    deYes_hs_breakdown_totals = de_yes.groupby(groupby_col)['hs_total_enrollment'].sum()
    apYes_hs_breakdown_totals = ap_yes.groupby(groupby_col)['hs_total_enrollment'].sum()

    # Used to substantiate the DataFrame
    deYes_hs_enroll = de_yes.groupby(groupby_col)['hs_total_enrollment'].sum().rename('HS Students in DE Offering') # Based on the Averager Function
    deYes_hs_pct = round(deYes_hs_enroll / deYes_hs_total * 100, 1).rename('%HS Students in DE Offering')
    de_total_enrolls = de_yes.groupby(groupby_col)['de_total_enrollment'].sum().rename('DE Students')
    de_pcts = round(de_total_enrolls / de_total * 100, 1).rename('%Total DE Students')
    de_gap = (de_pcts - deYes_hs_pct).rename('DE Gap')
    de_participation = round(de_total_enrolls / deYes_hs_breakdown_totals * 100, 1).rename('DE Participation Rate')

    apYes_hs_enroll = ap_yes.groupby(groupby_col)['hs_total_enrollment'].sum().rename('HS Students in AP Offering') # Based on the Averager Function
    apYes_hs_pct = round(apYes_hs_enroll / apYes_hs_total * 100, 1).rename('%HS Students in AP Offering')
    ap_total_enrolls = ap_yes.groupby(groupby_col)['ap_total_enrollment'].sum().rename('AP Students')
    ap_pcts = round(ap_total_enrolls / ap_total * 100, 1).rename('%Total AP Students')
    ap_gap = (ap_pcts - apYes_hs_pct).rename('AP Gap')
    ap_participation = round(ap_total_enrolls / apYes_hs_breakdown_totals * 100, 1).rename('AP Participation Rate')

    return pd.concat([deYes_hs_enroll, deYes_hs_pct, de_total_enrolls, de_pcts, de_gap, de_participation,
                      apYes_hs_enroll, apYes_hs_pct, ap_total_enrolls, ap_pcts, ap_gap, ap_participation], axis = 1)

def by_offering_enrollment_by_group_compiler(de_yes, ap_yes, groupby_col, group_abbr):
    """Used in the "By Offering" Enrollment Analyses Files to create DataFrames with the exact structures (can only be used for
        group attributes of a school (not students -- see the enrollment_compiler_layerer function))

        Inputs a DataFrame (dataset) and a Column in the DataFrame to perform a groupby() (groupby_col)

        Returns a Fully compiled DataFrame"""
    # These are used for calculating Ratios, Gaps, and Participation Rates
    deYes_hs_total = de_yes['hs_' + group_abbr].sum()
    apYes_hs_total = ap_yes['hs_' + group_abbr].sum()
    de_total = de_yes['de_' + group_abbr + '_enrollment'].sum()
    ap_total = ap_yes['ap_' + group_abbr + '_enrollment'].sum()

    deYes_hs_breakdown_totals = de_yes.groupby(groupby_col)['hs_' + group_abbr].sum()
    apYes_hs_breakdown_totals = ap_yes.groupby(groupby_col)['hs_' + group_abbr].sum()

    # Used to substantiate the DataFrame
    deYes_hs_enroll = de_yes.groupby(groupby_col)['hs_' + group_abbr].sum().rename('HS ' + group_abbr + ' Students in DE Offering').astype(int) # Based on the Averager Function
    deYes_hs_pct = round(deYes_hs_enroll / deYes_hs_total * 100, 1).rename('%HS ' + group_abbr + ' Students in DE Offering')
    de_total_enrolls = de_yes.groupby(groupby_col)['de_' + group_abbr + '_enrollment'].sum().rename('DE ' + group_abbr + ' Students')
    de_pcts = round(de_total_enrolls / de_total * 100, 1).rename('%Total ' + group_abbr + ' DE Students')
    de_gap = (de_pcts - deYes_hs_pct).rename(group_abbr + ' DE Gap')
    de_participation = round(de_total_enrolls / deYes_hs_breakdown_totals * 100, 1).rename('DE ' + group_abbr + ' Participation Rate')

    apYes_hs_enroll = ap_yes.groupby(groupby_col)['hs_' + group_abbr].sum().rename('HS ' + group_abbr + ' Students in AP Offering').astype(int) # Based on the Averager Function
    apYes_hs_pct = round(apYes_hs_enroll / apYes_hs_total * 100, 1).rename('%HS ' + group_abbr + ' Students in AP Offering')
    ap_total_enrolls = ap_yes.groupby(groupby_col)['ap_' + group_abbr + '_enrollment'].sum().rename('AP ' + group_abbr + ' Students')
    ap_pcts = round(ap_total_enrolls / ap_total * 100, 1).rename('%Total ' + group_abbr + ' AP Students')
    ap_gap = (ap_pcts - apYes_hs_pct).rename(group_abbr + ' AP Gap')
    ap_participation = round(ap_total_enrolls / apYes_hs_breakdown_totals * 100, 1).rename('AP ' + group_abbr + ' Participation Rate')

    return pd.concat([deYes_hs_enroll, deYes_hs_pct, de_total_enrolls, de_pcts, de_gap, de_participation,
                      apYes_hs_enroll, apYes_hs_pct, ap_total_enrolls, ap_pcts, ap_gap, ap_participation], axis = 1)

def by_offering_enrollment_compiler_layerer(de_yes, ap_yes, hs_col, de_col, ap_col, row_name):
    """Used in the Enrollment Analyses Files to create DataFrames with the exact structures (can only be used for
        student attributes of a school (not students -- see the enrollment_compiler function)) -- this function
        can only handle one 'row at a time', and the compiled DataFrame needs to be created using the
        pd.Concat() function.

        Inputs a DataFrame (dataset), a High School Enrollment column (hs_col),
            a DE Enrollment column (de_col), an AP Enrollment column (ap_col), and
            the string name of a row that is used for the index (row_name)

        Returns a one-rowed DataFrame"""
    # These are used for calculating Ratios, Gaps, and Participation Rates
    deYes_hs_total = de_yes['hs_total_enrollment'].sum()
    apYes_hs_total = ap_yes['hs_total_enrollment'].sum()
    de_total = de_yes['de_total_enrollment'].sum()
    ap_total = ap_yes['ap_total_enrollment'].sum()

    # Used to substantiate the DataFrame
    deYes_hs_enrolls = de_yes[hs_col].sum() # Based on the Averager Function
    deYes_hs_pcts = round(deYes_hs_enrolls / deYes_hs_total * 100, 1)
    de_total_enrolls = de_yes[de_col].sum()
    de_pcts = round(de_total_enrolls / de_total * 100, 1)
    de_gap = (de_pcts - deYes_hs_pcts)
    de_participation = round(de_total_enrolls / deYes_hs_enrolls * 100, 1)

    apYes_hs_enrolls = ap_yes[hs_col].sum() # Based on the Averager Function
    apYes_hs_pcts = round(apYes_hs_enrolls / apYes_hs_total * 100, 1)
    ap_total_enrolls = ap_yes[ap_col].sum()
    ap_pcts = round(ap_total_enrolls / ap_total * 100, 1)
    ap_gap = (ap_pcts - apYes_hs_pcts)
    ap_participation = round(ap_total_enrolls / apYes_hs_enrolls * 100, 1)

    order = ['HS Students in DE Offering','%HS Students in DE Offering', 'DE Students', '%Total DE Students', 'DE Gap','DE Participation Rate',
             'HS Students in AP Offering','%HS Students in AP Offering', 'AP Students', '%Total AP Students', 'AP Gap', 'AP Participation Rate']
    return pd.DataFrame({'HS Students in DE Offering': [deYes_hs_enrolls],
                  '%HS Students in DE Offering': [deYes_hs_pcts],
                  'DE Students': [de_total_enrolls],
                  '%Total DE Students': [de_pcts],
                  'DE Gap': [de_gap],
                  'DE Participation Rate': [de_participation],
                  'HS Students in AP Offering': [apYes_hs_enrolls],
                  '%HS Students in AP Offering': [apYes_hs_pcts],
                  'AP Students': [ap_total_enrolls],
                  '%Total AP Students': [ap_pcts],
                  'AP Gap': [ap_gap],
                  'AP Participation Rate': [ap_participation]},
                 index = [row_name])[order]
