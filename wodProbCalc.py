import argparse
import random

def roll_d10():
    return random.randint(1, 10)

def simulate_die(difficulty):
    roll = roll_d10()
    successes = 0
    cancels = 0
    if roll == 1:
        cancels += 1
    elif roll >= difficulty:
        successes += 1
    while roll == 10:
        roll = roll_d10()
        if roll == 1:
            cancels += 1
        elif roll >= difficulty:
            successes += 1
    return successes, cancels

def simulate_rolls(num_dice, difficulty, trials=1000000):
    success_counts = {}
    for _ in range(trials):
        total_successes = 0
        total_cancels = 0
        for _ in range(num_dice):
            s, c = simulate_die(difficulty)
            total_successes += s
            total_cancels += c
        net_successes = total_successes - total_cancels
        success_counts[net_successes] = success_counts.get(net_successes, 0) + 1
    return success_counts

def prob_at_least(success_counts, K, trials):
    count = sum(success_counts.get(key, 0) for key in success_counts if key >= K)
    return count / trials * 100

def main():
    parser = argparse.ArgumentParser(description="Calculate dice roll success probabilities.")
    parser.add_argument("--dice", type=int, required=True, help="Number of dice to roll")
    parser.add_argument("--difficulty", type=int, required=True, help="Difficulty threshold (2-10)")
    parser.add_argument("--trials", type=int, default=1000000, help="Number of simulation trials")
    parser.add_argument("--at-least", type=int, help="Also compute probability of at least this many successes")
    args = parser.parse_args()

    if args.dice < 1:
        print("Error: Number of dice must be at least 1.")
        return
    if args.difficulty < 2 or args.difficulty > 10:
        print("Error: Difficulty must be between 2 and 10.")
        return
    if args.trials < 1:
        print("Error: Number of trials must be at least 1.")
        return

    success_counts = simulate_rolls(args.dice, args.difficulty, args.trials)
    trials = args.trials  # Using the input trials directly for consistency

    print(f"With {args.dice} dice, difficulty {args.difficulty}:")
    for K in [1, 2, 3]:
        prob = prob_at_least(success_counts, K, trials)
        suffix = "es" if K > 1 else ""
        print(f"  At least {K} success{suffix}: Net successes ≥ {K}: {prob:.2f}%")

    if args.at_least is not None:
        K = args.at_least
        prob = prob_at_least(success_counts, K, trials)
        suffix = "es" if K > 1 else ""
        print(f"  At least {K} success{suffix}: Net successes ≥ {K}: {prob:.2f}%")

if __name__ == "__main__":
    main()
