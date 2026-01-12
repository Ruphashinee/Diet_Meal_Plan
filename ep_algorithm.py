import numpy as np

class EP_Optimizer:
    def __init__(self, menu_df, target_cal, target_prot, target_fat):
        self.df = menu_df
        self.target_cal = target_cal
        self.target_prot = target_prot
        self.target_fat = target_fat

    def fitness(self, individual):
        # individual is now just a list with ONE value: the row index
        idx = individual[0] % len(self.df)
        row = self.df.iloc[idx]
        
        t_price = row['Price_RM']
        t_cal = row['Calories']
        t_prot = row['Protein']
        t_fat = row['Fat']
        
        # Constraints/Penalties (Same logic, different targets)
        cal_penalty = abs(t_cal - self.target_cal) * 5
        prot_penalty = max(0, self.target_prot - t_prot) * 10 
        fat_penalty = max(0, t_fat - self.target_fat) * 10   
        
        return t_price + cal_penalty + prot_penalty + fat_penalty

    def run(self, generations=100, pop_size=50, mut_rate=0.3):
        # Initialize population with single indices
        pop = [[np.random.randint(0, len(self.df))] for _ in range(pop_size)]
        history = []
        
        for g in range(generations):
            offspring = []
            for parent in pop:
                child = parent.copy()
                if np.random.rand() < mut_rate:
                    # Mutate the row selection
                    child[0] = np.random.randint(0, len(self.df))
                offspring.append(child)
            
            combined = pop + offspring
            combined.sort(key=lambda x: self.fitness(x))
            pop = combined[:pop_size]
            history.append(self.fitness(pop[0]))
            
        return pop[0], history
