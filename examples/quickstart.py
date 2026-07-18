from proteinmask import design_sequence, make_family

family = make_family(n=40)
print(design_sequence(family, seed=2))
