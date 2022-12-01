from panflute import Header

def get_exercise_for_element(elem, doc):
    """
    This method requires the exercises filter to be run first!
    """
    curr = elem
    while (curr):
        if type(curr) == Header and "exercise" in curr.classes:
            return doc.exercises[curr.attributes["id"]]
        curr = curr.prev
    return
