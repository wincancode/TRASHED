package gameLogic

// Level representa el estado de un nivel en el juego
type Level struct {
	CurrentLevel         int
	AsteroidsDestroyed   int
	AsteroidsToNextLevel int
	LevelUpMessageTimer  float64
	MinAsteroids         int
	DifficultyFactor     int
	Score			   int
}

// InitializeLevel inicializa un nuevo nivel
func InitializeLevel() Level {
	return Level{
		CurrentLevel:         1,
		AsteroidsDestroyed:   0,
		AsteroidsToNextLevel: 10,
		LevelUpMessageTimer:  0,
		MinAsteroids:         10,
		DifficultyFactor:     1,
	}
}

// UpdateLevel actualiza el progreso del nivel
func UpdateLevel(level *Level, destroyedCount int, asteroids map[int]*Asteroid) {
	level.AsteroidsDestroyed += destroyedCount
	if level.AsteroidsDestroyed >= level.AsteroidsToNextLevel {
		level.CurrentLevel++
		level.AsteroidsDestroyed = 0
		level.AsteroidsToNextLevel += 5
		level.LevelUpMessageTimer = 3.0
		IncreaseDifficulty(level, asteroids)
	}
}

// IncreaseDifficulty incrementa la dificultad del juego
func IncreaseDifficulty(level *Level, asteroids map[int]*Asteroid) {
	level.DifficultyFactor++

	// Incrementar la dificultad de los asteroides existentes
	for _, asteroid := range asteroids {
		asteroid.MaxHealth++
		asteroid.Health = asteroid.MaxHealth
		asteroid.Width += 5
		asteroid.Height += 5
	}
}

// GenerateAsteroids genera nuevos asteroides si el número es menor al mínimo
func GenerateAsteroids(level *Level, asteroids *[]Asteroid) {
	for len(*asteroids) < level.MinAsteroids {
		*asteroids = append(*asteroids, InitializeAsteroid(len(*asteroids), level.DifficultyFactor))
	}
}
