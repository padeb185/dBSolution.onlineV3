from django.shortcuts import render

# Create your views here.
def luhn_check(card_number):
    """Vérifie si le numéro de carte est valide selon l'algorithme de Luhn."""
    digits = [int(d) for d in str(card_number)]
    check_digit = digits.pop()  # dernier chiffre
    digits.reverse()

    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

    total = sum(digits) + check_digit
    return total % 10 == 0


def calculate_check_digit(partial_card):
    """Calcule le check digit d'un numéro de carte incomplet."""
    digits = [int(d) for d in str(partial_card)]
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
        numero = input("Entrez le numéro complet de la carte : ").replace(" ", "")
        if luhn_check(numero):
            print("✅ Carte VALIDE (check digit correct)")
        else:
            print("❌ Carte INVALIDE (check digit incorrect)")

    elif choix == "2":
        partial = input("Entrez le numéro de carte sans le dernier chiffre : ").replace(" ", "")
        check_digit = calculate_check_digit(partial)
        print(f"Le check digit calculé est : {check_digit}")
        print(f"Numéro complet de la carte : {partial}{check_digit}")

    else:
        print("Option invalide")


if __name__ == "__main__":
    main()
