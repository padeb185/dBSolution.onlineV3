def luhn_check(card_number: str) -> bool:
    """
    Vérifie si un numéro de carte est valide selon l'algorithme de Luhn.
    Ignore les espaces et les tirets.
    """
    # Nettoyer le numéro
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit() or len(card_number) < 12:
        return False

    digits = [int(d) for d in card_number]
    check_digit = digits.pop()  # dernier chiffre
    digits.reverse()

    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

    total = sum(digits) + check_digit
    return total % 10 == 0


def calculate_check_digit(partial_card: str) -> int:
    """
    Calcule le check digit pour un numéro de carte incomplet.
    Ignore les espaces et les tirets.
    """
    partial_card = partial_card.replace(" ", "").replace("-", "")
    if not partial_card.isdigit():
        raise ValueError("Le numéro doit contenir uniquement des chiffres, espaces ou tirets autorisés.")

    digits = [int(d) for d in partial_card]
    digits.reverse()

    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

    total = sum(digits)
    check_digit = (10 - (total % 10)) % 10
    return check_digit


def main():
    print("=== Vérificateur / Calculateur de check digit carte bancaire ===")
    choix = input("Tapez 1 pour vérifier un numéro complet, 2 pour calculer le check digit : ")

    if choix == "1":
        numero = input("Entrez le numéro complet de la carte : ")
        if luhn_check(numero):
            print("✅ Carte VALIDE (check digit correct)")
        else:
            print("❌ Carte INVALIDE (check digit incorrect)")

    elif choix == "2":
        partial = input("Entrez le numéro de carte sans le dernier chiffre : ")
        check_digit = calculate_check_digit(partial)
        print(f"Le check digit calculé est : {check_digit}")
        print(f"Numéro complet de la carte : {partial.replace(' ', '').replace('-', '')}{check_digit}")

    else:
        print("Option invalide")


if __name__ == "__main__":
    main()




"""
Algorithme de Luhn (Check Digit)

On prend tous les chiffres de la carte sauf le dernier (c’est le check digit).

On part de la droite et on double tous les chiffres en position paire (en commençant par 0 à droite).

Si le double est ≥ 10, on soustrait 9.

On somme tous les chiffres.

Le check digit est le chiffre qui permet à la somme totale d’être un multiple de 10 :

\text{check_digit} = (10 - (somme\_totale \% 10)) \% 10

"""