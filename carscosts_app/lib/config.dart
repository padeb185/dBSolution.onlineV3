/// Adresse de l'API Django (espace particuliers).
///
/// Production (défaut) : https://carscosts.com/api/v1
/// Développement :
///   flutter run --dart-define=API_URL=http://127.0.0.1:8000/api/v1        (iOS, macOS, Windows)
///   flutter run --dart-define=API_URL=http://10.0.2.2:8000/api/v1         (émulateur Android)
const String apiUrl = String.fromEnvironment('API_URL', defaultValue: 'https://carscosts.com/api/v1');
