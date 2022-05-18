


##########################################################
############## Defining Surface ##########################
##########################################################
# creating the surface
surface = lambda s, t: [s+t, -s, t]
##########################################################
############## Defining Surface ##########################
##########################################################



##########################################################
############## Run Calculation ###########################
##########################################################
#running z2pack calculations
os.makedirs('results', exist_ok=True)
res_plus = z2pack.surface.run(
    system=snte_plus,
    surface=surface,
    save_file='results/res_plus_mz.json',
    load=True,
    **settings
)

res_minus = z2pack.surface.run(
    system=snte_minus,
    surface=surface,
    save_file='results/res_minus_mz.json',
    load=True,
    **settings
)
##########################################################
############## Run Calculation ###########################
##########################################################


##########################################################
############## Plot and Print ############################
##########################################################
# printing the Chern numbers
print('Chern number for +i eigenstates:', z2pack.invariant.chern(res_plus))
print('Chern number for -i eigenstates:', z2pack.invariant.chern(res_minus))

# creating plots
fig = plt.figure()
ax = fig.add_subplot(1, 2, 1)
ax.set_title("Chern number= {:5.3f}".format(z2pack.invariant.chern(res_plus)))
z2pack.plot.wcc(res_plus, axis=ax, gaps=False)
z2pack.plot.chern(res_plus, axis=ax)

ax = fig.add_subplot(1, 2, 2)
ax.set_title("Chern number= {:5.3f}".format(z2pack.invariant.chern(res_minus)))
z2pack.plot.wcc(res_minus, axis=ax, gaps=False)
z2pack.plot.chern(res_minus, axis=ax)

os.makedirs('plots', exist_ok=True)
plt.savefig('plots/plot_mz.png', bbox_inches='tight')
##########################################################
############## Plot and Print ############################
##########################################################

