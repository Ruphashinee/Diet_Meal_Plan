import numpy as np

class EP_Optimizer:
    def __init__(self, menu_df, target_cal, target_prot, target_fat):
        self.df = menu_df
        self.target_cal = target_cal
        self.target_prot = target_prot
        self.target_fat = target_fat

    def fitness(self, idx):
        # Get the full daily block from the CSV
        row = self.df.iloc[int(idx) % len(self.df)]
        
        t_price = row['Price_RM']
        t_cal = row['Calories']
        t_prot = row['Protein']
        t_fat = row['Fat']
        
        # Penalties for deviating from targets
        cal_diff = abs(t_cal - self.target_cal)
        prot_gap = max(0, self.target_prot - t_prot)
        fat_gap = max(0, t_fat - self.target_fat)
        
        # Total fitness score (Lower is better)
        return t_price + (cal_diff * 5) + (prot_gap * 10) + (fat_gap * 10)

    def run(self, generations=100, pop_size=50, mut_rate=0.3):
        # Initial population: random row indices
        pop = np.random.randint(0, len(self.df), size=pop_size)
        history = []
        
        for g in range(generations):
            offspring = []
            for parent in pop:
                # Mutation: occasionally jump to a new random row
                if np.random.rand() < mut_rate:
                    offspring.append(np.random.randint(0, len(self.df)))
                else:
                    offspring.append(parent)
            
            # Combine and select best survivors (Tournament selection)
            combined = np.concatenate([pop, offspring])
            combined = sorted(combined, key=lambda x: self.fitness(x))
            pop = combined[:pop_size]
            history.append(self.fitness(pop[0]))
            
        return pop[0], history
