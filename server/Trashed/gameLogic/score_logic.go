package gameLogic

// PlayerScore representa la puntuación de un jugador
type PlayerScore struct {
	PlayerUUID string
	Score      int
}

// AddScore agrega puntos a la puntuación de un jugador
func AddScore(scores *[]PlayerScore, playerUUID string, points int) {
	for i := 0; i < len(*scores); i++ {
		if (*scores)[i].PlayerUUID == playerUUID {
			(*scores)[i].Score += points
			return
		}
	}

	// Si el jugador no tiene una entrada, agregarlo
	*scores = append(*scores, PlayerScore{
		PlayerUUID: playerUUID,
		Score:      points,
	})
}

// GetPlayerScore obtiene la puntuación de un jugador
func GetPlayerScore(scores []PlayerScore, playerUUID string) int {
	for _, score := range scores {
		if score.PlayerUUID == playerUUID {
			return score.Score
		}
	}
	return 0
}

// GetTopScores devuelve las puntuaciones más altas
func GetTopScores(scores []PlayerScore, top int) []PlayerScore {
	// Ordenar las puntuaciones de mayor a menor
	for i := 0; i < len(scores); i++ {
		for j := i + 1; j < len(scores); j++ {
			if scores[j].Score > scores[i].Score {
				scores[i], scores[j] = scores[j], scores[i]
			}
		}
	}

	// Devolver las primeras `top` puntuaciones
	if len(scores) > top {
		return scores[:top]
	}
	return scores
}

// HandleAsteroidDestroyedScore maneja la asignación de puntos al destruir un asteroide
func HandleAsteroidDestroyedScore(scores *[]PlayerScore, playerUUID string, asteroid *Asteroid) {
	points := asteroid.Width // Ejemplo: los puntos se basan en el tamaño del asteroide
	AddScore(scores, playerUUID, points)
}

// HandlePowerUpCollectedScore maneja la asignación de puntos al recoger un power-up
func HandlePowerUpCollectedScore(scores *[]PlayerScore, playerUUID string, powerUp *PowerUp) {
	points := 50 // Ejemplo: 50 puntos por recoger un power-up
	AddScore(scores, playerUUID, points)
}
