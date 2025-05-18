package main

import (
	"math"
	"math/rand"
	"time"
)

// CheckCollision verifica si dos rectángulos colisionan
func CheckCollision(x1, y1, w1, h1, x2, y2, w2, h2 float64) bool {
	return !(x1+w1/2 < x2-w2/2 || x1-w1/2 > x2+w2/2 || y1+h1/2 < y2-h2/2 || y1-h1/2 > y2+h2/2)
}

// HandleShipAsteroidCollisions maneja las colisiones entre una nave y asteroides
func HandleShipAsteroidCollisions(ship *ShipState, asteroids *[]Asteroid, releasedAsteroids *[]Asteroid) bool {
	for i := 0; i < len(*asteroids); i++ {
		asteroid := &(*asteroids)[i]
		if CheckCollision(ship.PosX, ship.PosY, 50, 50, asteroid.PosX, asteroid.PosY, float64(asteroid.Width), float64(asteroid.Height)) {
			if ship.ShieldActive {
				ship.ShieldCharges--
				if ship.ShieldCharges <= 0 {
					ship.ShieldActive = false
				}
				*releasedAsteroids = append(*releasedAsteroids, ReleaseAsteroids(ship, 8)...) // Liberar asteroides
				*asteroids = append((*asteroids)[:i], (*asteroids)[i+1:]...)                  // Eliminar asteroide
				return false                                                                  // No perder vida
			} else {
				ship.Lives--
				*asteroids = append((*asteroids)[:i], (*asteroids)[i+1:]...) // Eliminar asteroide
				return true                                                  // Perder vida
			}
		}
	}
	return false
}

// HandleBulletAsteroidCollisions maneja las colisiones entre balas y asteroides
func HandleBulletAsteroidCollisions(bullets *[]Bullet, asteroids *[]Asteroid, messages *[]string, powerups *[]PowerUp, releasedAsteroids *[]Asteroid) (int, int) {
	totalPoints := 0
	destroyedCount := 0

	for i := 0; i < len(*bullets); i++ {
		bullet := &(*bullets)[i]
		if !bullet.Active {
			continue
		}

		for j := 0; j < len(*asteroids); j++ {
			asteroid := &(*asteroids)[j]
			if CheckCollision(bullet.PosX, bullet.PosY, float64(bullet.Width), float64(bullet.Height), asteroid.PosX, asteroid.PosY, float64(asteroid.Width), float64(asteroid.Height)) {
				bullet.Active = false
				asteroid.Health -= bullet.Damage

				if asteroid.Health <= 0 {
					*asteroids = append((*asteroids)[:j], (*asteroids)[j+1:]...)
					destroyedCount++

					// Calcular puntos según el tamaño del asteroide
					points := asteroid.Width
					totalPoints += points

					// Agregar un mensaje temporal
					*messages = append(*messages, formatMessage("+"+string(points)+" puntos", 0))

					// Generar un power-up con probabilidad del 50%
					if rand.Float64() < 0.5 {
						powerType := []string{"laser_boost", "shield"}[rand.Intn(2)]
						*powerups = append(*powerups, GenerateRandomPowerUp(asteroid.PosX, asteroid.PosY))
					}
				}
				break
			}
		}
	}

	return totalPoints, destroyedCount
}

// HandlePowerUpCollisions maneja las colisiones entre una nave y los power-ups
func HandlePowerUpCollisions(ship *ShipState, powerups *[]PowerUp, messages *[]string) {
	for i := 0; i < len(*powerups); i++ {
		powerup := &(*powerups)[i]
		if CheckCollision(ship.PosX, ship.PosY, 50, 50, powerup.PosX, powerup.PosY, float64(powerup.Width), float64(powerup.Height)) {
			ApplyPowerUpEffect(ship, powerup, messages)
			*powerups = append((*powerups)[:i], (*powerups)[i+1:]...)
		}
	}
}

// ReleaseAsteroids genera asteroides secundarios alrededor de una nave
func ReleaseAsteroids(ship *ShipState, count int) []Asteroid {
	rand.Seed(time.Now().UnixNano())
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
