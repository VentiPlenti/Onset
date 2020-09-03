class Segment:
    '''A representation of a phonetic segment, stored in terms of features.'''

    __slots__ = ['_positive', '_negative', '_zero']

    def __init__(self, positive, negative, zero):
        self._positive = positive
        self._negative = negative
        self._zero = zero

    @classmethod
    def from_dictionary(cls, feature_dictionary):
        '''Initialise the segment from a dictionary of features. The feature name
        is the key, and the value is one of '+', '-', or '0'. The only ignored
        key is "IPA".'''

        positive = [key for key, value in feature_dictionary.items()
                    if value == '+']
        negative = [key for key, value in feature_dictionary.items()
                    if value == '-']
        zero = [key for key, value in feature_dictionary.items()
                    if value == '0']

        return cls(positive, negative, zero)

    @property
    def positive(self):
        return self._positive

    def add_positive(self, feature):
        '''Add the feature to the positive list. If it already exists in the
        negative or zero list, remove it from that list.'''

        if feature not in self._positive:
            if feature in self._negative:
                self._negative.remove(feature)
            #Zero feature needs to be added
            if feature in self._zero:
                self._zero.remove(feature)

            self._positive.append(feature)

    @property
    def negative(self):
        return self._negative

    def add_negative(self, feature):
        '''Add the feature to the negative list. If it already exists in the
        positive or zero list, remove it from that list.'''

        if feature not in self._negative:
            if feature in self._positive:
                self._positive.remove(feature)
            #Ditto. Hopefully this actually works
            if feature in self._zero:
                self._zero.remove(feature)

            self._negative.append(feature)
            
    #Adding the ability for a feature to be zero. 
    #This allows for much more flexibility in rule creation. Lots of pain to implement but it's hopefully worth it.
    @property
    def zero(self):
        return self._zero
        
    def add_zero(self, feature):
        '''Add the feature to the zero list. If it already exists in either the 
        positive or negative list, remove it from that list.'''
        
        if feature not in self._zero:
            if feature in self._positive:
                self._positive.remove(feature)
            if feature in self._negative:
                self._negative.remove(feature)
            
            self._zero.append(feature)

    def meets_conditions(self, conditions):
        '''Takes a dictionary of features, in the format:

            {'positive': ['feature1', 'feature2'], 'negative': ['feature3'], 'zero': ['feature4']}

        Returns True if all features specified as positive are in
        self._positive, those specified as negative are in self._negative, and those specified as zero are in self._zero.
        Otherwise returns false.

        '''

        # This code is really ugly. I had a cool one-liner using sets, but
        # switching to basic loops saved 8 seconds (!) when benchmarking.
        # Such is the life of optimisation.
        
        #Forker's note: Hope your optimization still lasts.
        if 'positive' in conditions:
            for feature in conditions['positive']:
                if feature not in self._positive:
                    return False

        if 'negative' in conditions:
            for feature in conditions['negative']:
                if feature not in self._negative:
                    return False
        
        if 'zero' in conditions:
            for feature in conditions['zero']:
                if feature not in self._zero:
                    return False

        return True

    def __add__(self, other):
        '''Override the regular addition behaviour. When two segments are added
        together, the values of the second override those of the first that
        differ.'''
        new_segment = Segment(self._positive.copy(), self._negative.copy(), self._zero.copy())

        for positive_feature in other.positive:
            new_segment.add_positive(positive_feature)

        for negative_feature in other.negative:
            new_segment.add_negative(negative_feature)
        
        for zero_feature in other.zero:
            new_segment.add_zero(zero_feature)

        return new_segment

    def __repr__(self):
        return '<Segment> Positive: {0}, Negative: {1}, Zero: {2}'.format(self._positive,
                                                               self._negative, self._zero)
