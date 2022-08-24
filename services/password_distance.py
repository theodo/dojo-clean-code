
def compute_levenshtein_distance(string1, string2):
    pass


if __name__ == "__main__":
    assert (compute_levenshtein_distance("Python", "Peithen") == 3)
    assert (compute_levenshtein_distance("Azerty12", "Azerty14") == 1)
    assert (compute_levenshtein_distance("Toto", "toto13") == 3)
    assert (compute_levenshtein_distance("JohnDoe2001", "Johndoe2002") == 2)
