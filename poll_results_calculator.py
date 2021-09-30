import math


class PollResultsCalculator:
    """Class which performs calculating of average characters rating and concordance factor for it"""
    def average_characters_rating_and_concordance_factor(self,
                                                         answers: list[tuple[int, int, float]],
                                                         characters_id: list[int]) -> (dict[int, float], float):
        """Performs calculation of final result of poll

        :param answers: list of tuples(character_a_id, character_b_id, ratio_a_to_b)
        :param characters_id: list of characters id
        :return: average_characters_rating: dictionary(character_id, rating), concordance_factor: float
        """

        ratio_matrix = self.__create_ratio_matrix(answers, characters_id)
        normalized_ratio_matrix = self.__normalize_ratio_matrix(ratio_matrix)
        average_characters_rating = self.__calculate_average_characters_rating(normalized_ratio_matrix)
        measures_of_consistency = self.__calculate_measures_of_consistency(ratio_matrix, average_characters_rating)
        concordance_factor = self.__calculate_concordance_factor(measures_of_consistency)

        return average_characters_rating, concordance_factor

    def __create_ratio_matrix(self,
                              answers: list[tuple[int, int, float]],
                              characters_id: list[int]) -> dict[int, dict[int, float]]:
        """Creates matrix with ratios from one character to another

        :param answers: list of tuples(character_a_id, character_b_id, ratio_a_to_b)
        :param characters_id: list of characters id
        :return: dictionary(character_id, dictionary(character_id, ratio))
        """

        ratio_matrix = {character_id: {} for character_id in characters_id}
        for answer in answers:
            ratio_matrix[answer[0]][answer[1]] = answer[2]
        return ratio_matrix

    def __normalize_ratio_matrix(self, ratio_matrix: dict[int, dict[int, float]]) -> dict[int, dict[int, float]]:
        """Normalizes matrix with ratios from one character to another

        :param ratio_matrix: dictionary(character_id, dictionary(character_id, ratio))
        :return: dictionary(character_id, dictionary(character_id, ratio))
        """

        normalized_ratio_matrix = {character_id: {} for character_id in ratio_matrix}

        for character_id in normalized_ratio_matrix:
            column_sum = sum((sub_dict[character_id] for sub_dict in ratio_matrix.values()))
            for key, sub_dict in normalized_ratio_matrix.items():
                sub_dict[character_id] = ratio_matrix[key][character_id] / column_sum
        return normalized_ratio_matrix

    def __calculate_average_characters_rating(self,
                                              normalized_ratio_matrix: dict[int, dict[int, float]]) -> dict[int, float]:
        """Returns average ratings for each character from ratio matrix"""

        average_characters_rating = {}

        for character_id, sub_dict in normalized_ratio_matrix.items():
            ratios = sub_dict.values()
            average_characters_rating[character_id] = sum(ratios) / len(ratios)
        return average_characters_rating

    def __calculate_measures_of_consistency(self,
                                            ratio_matrix: dict[int, dict[int, float]],
                                            average_characters_rating: dict[int, float]) -> dict[int, float]:
        """Defines measure of consistency for each character's average rating"""

        measures_of_consistency = {}

        for current_character_id, sub_dict in ratio_matrix.items():
            measure_of_consistency = 0
            for intermediate_character_id, ratio in sub_dict.items():
                measure_of_consistency += ratio * average_characters_rating[intermediate_character_id]
            measure_of_consistency /= average_characters_rating[current_character_id]
            measures_of_consistency[current_character_id] = measure_of_consistency
        return measures_of_consistency

    def __calculate_concordance_factor(self, measures_of_consistency: dict[int, float]) -> float:
        """Defines concordance factor for whole poll"""

        number_of_characters = len(measures_of_consistency)
        consistency_index = (sum(measures_of_consistency.values())
                             / number_of_characters - number_of_characters) / (number_of_characters - 1)
        randomization_index = self.__calculate_randomization_index(number_of_characters)
        return consistency_index / randomization_index

    def __calculate_randomization_index(self, number_of_characters: int) -> float:
        """Defines randomization index for certain number of characters"""

        return -0.4573 + 0.9034 * math.log(number_of_characters)
