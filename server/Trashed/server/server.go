package main

import (
	"Trashed/Trashed/gameLogic"
	"Trashed/Trashed/proto"
	"context"
	"fmt"
	"log"
	"math"
	"math/rand"
	"net"
	"sync"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/reflection"
)

type server struct {
	proto.UnimplementedGameServiceServer
	mu    sync.Mutex
	games map[string]game
}

type game struct {
	Data *proto.GameData
	SubscribedInputStreams map[string]proto.GameService_JoinInputUpdatesServer
	Ships map[string]*gameLogic.ShipState // key: playerUuid
	Asteroids map[int]*gameLogic.Asteroid // key: asteroidId
	Bullets map[int]*gameLogic.Bullet // key: bulletId
	PowerUps map[int]*gameLogic.PowerUp // key: powerUpId
	LatestInputs map[string]*proto.Input // Store latest input per player
	Level *gameLogic.Level // Game level state
}

func NewServer() *server {
	return &server{
		games: make(map[string]game),
	}
}

const (
	// Define the colors available for players
	Red    = "red"
	Green  = "green"
	Blue   = "blue"
	Yellow = "yellow"
)


func generateGameCode() string {
	rand.Seed(time.Now().UnixNano())
	const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	code := make([]byte, 6)
	for i := range code {
		code[i] = charset[rand.Intn(len(charset))]
	}


	//!!!!!!!!!!!!!!!!!!!!
	code = []byte("2")
	return string(code)
}

func (s *server) CreateGame(ctx context.Context, in *proto.Empty) (*proto.GameCode, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Generar un código único para la partida
	gameCode := generateGameCode()
	s.games[gameCode] = game{
		Data: &proto.GameData{
			Code:    gameCode,
			Players: []*proto.PlayerData{},
			Started: false,
		},
		SubscribedInputStreams: make(map[string]proto.GameService_JoinInputUpdatesServer),
	}

	log.Printf("Game created with code: %s", gameCode)
	return &proto.GameCode{Code: gameCode}, nil
}


func (s *server) JoinGame(in *proto.PlayerData, stream proto.GameService_JoinGameServer) error {
	gameCode := in.GameCode

	// Verificar si la partida existe
	s.mu.Lock()
	game, exists := s.games[gameCode]
	if !exists {
		s.mu.Unlock()
		log.Printf("Partida no encontrada: %s", gameCode)
		return fmt.Errorf("partida no encontrada")
	}

	//search for a color that is not used
	usedColors := make(map[string]bool)

	for _, player := range game.Data.Players {
		usedColors[player.Color] = true
	}

	availableColors := []string{Red, Green, Blue, Yellow}
	
	var selectedColor string
	
	for _, color := range availableColors {
		if !usedColors[color] {
			selectedColor = color
			break
		}
	}

	// Agregar el jugador a la partida
	player := &proto.PlayerData{
		PlayerUuid: in.PlayerUuid,
		Username:   in.Username,
		Color:      selectedColor,
		Slot:       int32(len(game.Data.Players)),
		GameCode:   gameCode,
	}
	game.Data.Players = append(game.Data.Players, player)
	s.mu.Unlock()

	log.Printf("Nuevo jugador agregado: %s, username: %s, slot: %d", player.PlayerUuid, player.Username, player.Slot)

	// Enviar actualizaciones de la lista de jugadores conectados
	for {
		s.mu.Lock()
		gameData := &proto.GameData{
			Code:    gameCode,
			Players: game.Data.Players,
			Started: game.Data.Started,
		}
		s.mu.Unlock()

		if err := stream.Send(gameData); err != nil {
			log.Printf("Error enviando datos de la partida: %v", err)
			return err
		}	

		time.Sleep(1 * time.Second) // Enviar actualizaciones cada segundo
	}
}


func (s *server) StartGame(ctx context.Context, in *proto.GameCode) (*proto.BoolMessage,error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	gameCode := in.Code
	game, exists := s.games[gameCode]
	if !exists {
		log.Printf("Partida no encontrada: %s", gameCode)
		return &proto.BoolMessage{Value: false}, fmt.Errorf("partida no encontrada")
	}

	// Initialize ShipStates for each player
	ships := make(map[string]*gameLogic.ShipState)
	for _, player := range game.Data.Players {
		ships[player.PlayerUuid] = &gameLogic.ShipState{
			PlayerUuid: player.PlayerUuid,
			PosX: 800/2,
			PosY: 600/2,
			Angle: 360,
			Speed: 0,
			LaserBoostLevel: 0,
			ShieldActive: false,
			ShieldCharges: 0,
			Lives: 3,
		}
	}
	game.Ships = ships
	game.Asteroids = make(map[int]*gameLogic.Asteroid)
	game.Bullets = make(map[int]*gameLogic.Bullet)
	game.PowerUps = make(map[int]*gameLogic.PowerUp)
	game.Level = &gameLogic.Level{
		CurrentLevel:         1,
		AsteroidsDestroyed:   0,
		AsteroidsToNextLevel: 10,
		LevelUpMessageTimer:  0,
		MinAsteroids:         10,
		DifficultyFactor:     1,
		Score: 0,
	}
	
	// Initialize LatestInputs map
	game.LatestInputs = make(map[string]*proto.Input)
	s.games[gameCode] = game

	// Mark game as started
	game.Data.Started = true

	// Start the fixed-tick game loop
	go s.runGameLoop(gameCode)

	log.Printf("Partida iniciada: %s", gameCode)
	return &proto.BoolMessage{Value: true}, nil;
}


// Fixed-tick game loop for each game
func (s *server) runGameLoop(gameCode string) {
	ticker := time.NewTicker(time.Second / 60) // 60 FPS
	defer ticker.Stop()
	var lastTick = time.Now()
	for {
		<-ticker.C
		deltaTime := time.Since(lastTick).Seconds()
		lastTick = time.Now()
		s.mu.Lock()
		game, exists := s.games[gameCode]
		if !exists || !game.Data.Started {
			s.mu.Unlock()
			return
		}

		
		// Convert maps to slices for collision logic
		bullets := make([]gameLogic.Bullet, 0, len(game.Bullets))
		for _, b := range game.Bullets {
			if b != nil {
				bullets = append(bullets, *b)
			}
		}
		asteroids := make([]gameLogic.Asteroid, 0, len(game.Asteroids))
		for _, a := range game.Asteroids {
			if a != nil {
				asteroids = append(asteroids, *a)
			}
		}
		powerUps := make([]gameLogic.PowerUp, 0, len(game.PowerUps))
		for _, p := range game.PowerUps {
			if p != nil {
				powerUps = append(powerUps, *p)
			}
		}
		
		
		
		//*Game functionalities
		
		//instantiate bullets 
		for playerID, ship := range game.Ships {
			input := game.LatestInputs[playerID]
			if input == nil {
				input = &proto.Input{}
			}
			if input.IsShoot && ship.LastShotTime.Add(200*time.Millisecond).Before(time.Now()) {
				bullet := gameLogic.InitializeBullet(ship.PosX, ship.PosY, ship.Angle, game.Level.DifficultyFactor)
				bulletID := len(game.Bullets) + 1
				game.Bullets[bulletID] = &bullet
				game.Ships[playerID].LastShotTime = time.Now()
			}
		}

		//update bullets
		for id, bullet := range game.Bullets {
			if bullet != nil {
				gameLogic.UpdateBulletPosition(bullet, deltaTime,1000,1000)
				if !bullet.Active {
					delete(game.Bullets, id)
				}
			}
		}
		
		//manage asteroid collisions with bullets, score and difficulty logic
		points, destroyed_count := gameLogic.HandleBulletAsteroidCollisions(
			&bullets,
			&asteroids,
			&powerUps,
		)

		game.Level.AsteroidsDestroyed += destroyed_count
		game.Level.AsteroidsToNextLevel -= destroyed_count
		if game.Level.AsteroidsToNextLevel <= 0 {
			game.Level.CurrentLevel++
			game.Level.AsteroidsToNextLevel = 10 + game.Level.CurrentLevel*5
			game.Level.MinAsteroids += 5
			game.Level.DifficultyFactor++
		}

		game.Level.LevelUpMessageTimer -= deltaTime
		if game.Level.LevelUpMessageTimer <= 0 {
			game.Level.LevelUpMessageTimer = 0
		}

		game.Level.Score += points


		
		//Manage ASteroid and bullet collisions
		
		// # Manejar colisiones entre balas y asteroides
        // # for ship in ships:
        // #     points, destroyed_count = handle_bullet_asteroid_collisions(ship.bullets, asteroids, messages, powerups, released_asteroids)
        // #     score += points  # Sumar los puntos obtenidos al puntaje total
        // #     level.update(destroyed_count, asteroids)  # Actualizar el progreso del nivel

        // # Generar nuevos asteroides si el número es menor al mínimo
        // # while len(asteroids) < level.min_asteroids:
        // #      asteroids.append(Asteroid(len(asteroids), difficulty_factor=level.difficulty_factor))



		//*Updates

		// Update all ships
		for playerID, ship := range game.Ships {
			input := game.LatestInputs[playerID]
			if input == nil {
				input = &proto.Input{}
			}
			game.Ships[playerID] = gameLogic.UpdateShipPosition(ship, input, deltaTime)
		}


		// Convert all ShipStates to proto.PlayerStates
		playerStates := AllShipsToProtoStates(game.Ships, gameCode)
		// Convert all AsteroidStates to proto.AsteroidStates
		asteroidStates := AllAsteroidsToProtoStates(game.Asteroids)
		// Convert all BulletStates to proto.BulletStates
		bulletStates := AllBulletsToProtoStates(game.Bullets)
		// Convert all PowerUpStates to proto.PowerUpStates
		powerUpStates := AllPowerUpsToProtoStates(game.PowerUps)
		// Convert Level to proto.Level
		levelState := LevelToProto(game.Level)


		// Compose GameState
		gameState := &proto.GameState{
			PlayerStates: playerStates,
			Asteroids: asteroidStates,
			Bullets: bulletStates,
			Powerups: powerUpStates,
			Level:  levelState,
		}
		// Broadcast updated state to all subscribed players
		for _, subStream := range game.SubscribedInputStreams {
			err := subStream.Send(gameState)
			if err != nil {
				log.Printf("Error sending state to player: %v", err)
			}
		}
		s.games[gameCode] = game
		s.mu.Unlock()
	}
}

//Helper: convert Level to proto.Level
func LevelToProto(level *gameLogic.Level) *proto.LevelState {
	return &proto.LevelState{
		CurrentLevel:         int32(level.CurrentLevel),
		AsteroidsDestroyed:   int32(level.AsteroidsDestroyed),
		AsteroidsToNextLevel: int32(level.AsteroidsToNextLevel),
		LevelUpMessageTimer:  level.LevelUpMessageTimer,
	}
}

// Helper: Convert ShipState to proto.PlayerState
func ShipStateToProto(playerUuid string, ship *gameLogic.ShipState, code string) *proto.PlayerState {
	return &proto.PlayerState{
		Code: code,
		PlayerUuid: playerUuid,
		Timestamp: time.Now().Unix(),
		Position: &proto.Position{
			X: ship.PosX,
			Y: ship.PosY,
			Angle: ship.Angle,
			SpeedX: ship.Speed * math.Sin(degreesToRadians(ship.Angle)),
			SpeedY: -ship.Speed * math.Cos(degreesToRadians(ship.Angle)),
			AccelerationX: 0, // You can add this if you store it in ShipState
			AccelerationY: 0,
		},
	}
}

func degreesToRadians(degrees float64) float64 {
	return degrees * math.Pi / 180
}

// Helper: Convert all ShipStates to proto.PlayerStates map
func AllShipsToProtoStates(ships map[string]*gameLogic.ShipState, code string) map[string]*proto.PlayerState {
	states := make(map[string]*proto.PlayerState)
	for uuid, ship := range ships {
		states[uuid] = ShipStateToProto(uuid, ship, code)
	}
	return states
}

// Helper: Convert Asteroid to proto.AsteroidState
func AsteroidStateToProto(id int, asteroid *gameLogic.Asteroid) *proto.AsteroidState {
	return &proto.AsteroidState{
		Id: int32(asteroid.ID),
		X: asteroid.PosX,
		Y: asteroid.PosY,
		Width: int32(asteroid.Width),
		Height: int32(asteroid.Height),
		Speed: asteroid.Speed,
		Angle: asteroid.Angle,
		Health: int32(asteroid.Health),
		MaxHealth: int32(asteroid.MaxHealth),
	}
}

func AllAsteroidsToProtoStates(asteroids map[int]*gameLogic.Asteroid) []*proto.AsteroidState {
	states := make([]*proto.AsteroidState, 0, len(asteroids))
	for id, asteroid := range asteroids {
		states = append(states, AsteroidStateToProto(id, asteroid))
	}
	return states
}

// Helper: Convert Bullet to proto.BulletState
func BulletStateToProto(id int, bullet *gameLogic.Bullet) *proto.BulletState {
	return &proto.BulletState{
		Id: int32(id),
		X: bullet.PosX,
		Y: bullet.PosY,
		Angle: bullet.Angle,
		Speed: bullet.Speed,
		Active: bullet.Active,
		Damage: int32(bullet.Damage),
		Width: int32(bullet.Width),
		Height: int32(bullet.Height),
	}
}

func AllBulletsToProtoStates(bullets map[int]*gameLogic.Bullet) []*proto.BulletState {
	states := make([]*proto.BulletState, 0, len(bullets))
	for id, bullet := range bullets {
		states = append(states, BulletStateToProto(id, bullet))
	}
	return states
}

// Helper: Convert PowerUp to proto.PowerUpState
func PowerUpStateToProto(id int, powerup *gameLogic.PowerUp) *proto.PowerUpState {
	return &proto.PowerUpState{
		Id: int32(id),
		X: powerup.PosX,
		Y: powerup.PosY,
		Type: powerup.Type,
		Width: int32(powerup.Width),
		Height: int32(powerup.Height),
		Active: powerup.Active,
	}
}

func AllPowerUpsToProtoStates(powerups map[int]*gameLogic.PowerUp) []*proto.PowerUpState {
	states := make([]*proto.PowerUpState, 0, len(powerups))
	for id, powerup := range powerups {
		states = append(states, PowerUpStateToProto(id, powerup))
	}
	return states
}

func (s *server) JoinInputUpdates(stream proto.GameService_JoinInputUpdatesServer) error {
	md,ok := metadata.FromIncomingContext(stream.Context())
	if !ok {
		return fmt.Errorf("metadata not found")
	}
	gameCode := md.Get("game_code")
	playerUuid := md.Get("player_uuid")
	if len(playerUuid) == 0 {
		return fmt.Errorf("player uuid not found")
	}
	if len(gameCode) == 0 {
		return fmt.Errorf("game code not found")
	}
	gameCodeStr := gameCode[0]
	playerUuidStr := playerUuid[0]
	log.Printf("Player UUID: %s, Game Code: %s", playerUuidStr, gameCodeStr)
	// Subscribe the player to input updates
	s.mu.Lock()
	game, exists := s.games[gameCodeStr]
	if !exists {
		s.mu.Unlock()
		log.Printf("Partida no encontrada: %s", gameCodeStr)
		return fmt.Errorf("partida no encontrada")
	}
	if _, exists := game.SubscribedInputStreams[playerUuidStr]; exists {
		s.mu.Unlock()
		log.Printf("Player already subscribed: %s", playerUuidStr)
		return fmt.Errorf("player already subscribed")
	}
	game.SubscribedInputStreams[playerUuidStr] = stream
	s.games[gameCodeStr] = game
	s.mu.Unlock()
	log.Printf("Player subscribed to input updates: %s", playerUuidStr)
	// Only store latest input per player
	for {
		in, err := stream.Recv()
		if err != nil {
			return err
		}
		s.mu.Lock()
		game, exists := s.games[gameCodeStr]
		if exists {
			game.LatestInputs[in.PlayerUuid] = in.Input
			s.games[gameCodeStr] = game
		}
		s.mu.Unlock()
	}
}


func main() {
	// Create a new gRPC server
	s := grpc.NewServer()
	proto.RegisterGameServiceServer(s, NewServer())

	reflection.Register(s)

	// Listen on port 50051
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	log.Println("Server is running on port 50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
