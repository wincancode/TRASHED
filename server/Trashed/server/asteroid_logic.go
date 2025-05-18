package main

import (
	"math"
	"math/rand"
	"time"
)

// Asteroid representa un asteroide en el juego
type Asteroid struct {
	ID        int
	PosX      float64
	PosY      float64
	Width     int
	Height    int
	Speed     float64
	Angle     float64
	Health    int
	MaxHealth int
}

// InitializeAsteroid genera un nuevo asteroide con propiedades aleatorias
func InitializeAsteroid(id int, difficultyFactor int) Asteroid {
	rand.Seed(time.Now().UnixNano())
	baseSize := rand.Intn(30) + 20
	return Asteroid{
		ID:        id,
		Width:     baseSize + difficultyFactor*5,
		Height:    baseSize + difficultyFactor*5,
		PosX:      float64(rand.Intn(800)), // Ejemplo: ancho del juego
		PosY:      float64(rand.Intn(600)), // Ejemplo: alto del juego
		Speed:     rand.Float64()*100 + 50,
		Angle:     rand.Float64() * 360,
		Health:    (baseSize / 10) + difficultyFactor,
		MaxHealth: (baseSize / 10) + difficultyFactor,
	}
}

// UpdateAsteroidPosition actualiza la posición del asteroide
func UpdateAsteroidPosition(asteroid *Asteroid, deltaTime float64) {
	asteroid.PosX += asteroid.Speed * math.Cos(asteroid.Angle*math.Pi/180) * deltaTime
	asteroid.PosY += asteroid.Speed * math.Sin(asteroid.Angle*math.Pi/180) * deltaTime
}

// CheckCollision verifica si un asteroide colisiona con una nave
func CheckCollision(ship *ShipState, asteroid *Asteroid) bool {
	shipLeft := ship.PosX - 25 // Asumiendo un ancho fijo de 50 para la nave
	shipRight := ship.PosX + 25
	shipTop := ship.PosY - 25 // Asumiendo un alto fijo de 50 para la nave
	shipBottom := ship.PosY + 25

	asteroidLeft := asteroid.PosX - float64(asteroid.Width)/2
	asteroidRight := asteroid.PosX + float64(asteroid.Width)/2
	asteroidTop := asteroid.PosY - float64(asteroid.Height)/2
	asteroidBottom := asteroid.PosY + float64(asteroid.Height)/2

	return !(shipRight < asteroidLeft || shipLeft > asteroidRight || shipBottom < asteroidTop || shipTop > asteroidBottom)
}

// ReleaseAsteroids genera asteroides alrededor de una nave
func ReleaseAsteroids(ship *ShipState, count int) []Asteroid {
	asteroids := []Asteroid{}
	safeRadius := 50.0
	for i := 0; i < count; i++ {
		angle := float64(i) * (360.0 / float64(count))
		asteroid := InitializeAsteroid(-1, 0)
		asteroid.PosX = ship.PosX + safeRadius*math.Cos(angle*math.Pi/180)
		asteroid.PosY = ship.PosY + safeRadius*math.Sin(angle*math.Pi/180)
		asteroid.Speed = 200
		asteroid.Health = 1
		asteroid.MaxHealth = 1
		asteroids = append(asteroids, asteroid)
	}
	return asteroids
}
