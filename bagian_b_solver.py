from sympy import factorint 

n = 42637272
  
factor_dict = factorint(n)
# factor_dict = {2: 3, 3: 1, 47: 1, 37799: 1} {1128: 1, 37799: 1}
print(factor_dict)

# a = 1128
ae_mod_n = 101757372914892934470838335192136609818834150239471897190313164909116616821784351223832084385554211466714743065518774472425267416565624413629848292082812372108457217034890293916633236618635994863820346891298541846116849707272680901319144535567776980727791367932302521944845879721571212404407698798791577471180
# b = 37799
be_mod_n = 114855021896112129632823958134103744577648187111485442109561499599825777416973342666448943244806410003264702493484820482469014147460039610554851519522316017151238426478968524025189889370811216367943025084827543490219116386659319005460949063326696674467133060332393536267501469575309623012663936436696984556711

print(ae_mod_n*be_mod_n)

# ae_mod_n*be_mod_n
# 11687345294230875350005907689148907003794012720489408523464976063264597441200103415954694745288080186114727439842090725314847629626627858137114231232943119245828617237025372933853972613605715087902395098392538699591415489072492262764904802993625593242964652553595573668597009847066330574695676842198706053164247227817897854327806062106330750856990356404179002357747937503684889447183054642464687515496665737655011606356383464374309886455571135288056012066769922765668898579950981859788276608850298001498962996453263372242897044937865898615465817662365438791632345608212392084118413338894180256984496720710806678088980