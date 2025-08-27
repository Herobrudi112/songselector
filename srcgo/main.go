package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"

	"github.com/gorilla/mux"
)

type Song struct {
	Name     string `json:"name"`
	Token    int    `json:"token"`
	Type     string `json:"type"`
	Artist   string `json:"artist"`
	Title    string `json:"title"`
	Start    string `json:"start"`
	ItunesId string `json:"itunesId,omitempty"`
	Link     string `json:"link,omitempty"`
}

var baseDir, _ = os.Getwd()
var songSubmissionsFile = filepath.Join(baseDir, "song_submissions.json")
var tokensFile = filepath.Join(baseDir, "tokens.json")

func checkToken(token int) bool {
	data, err := os.ReadFile(tokensFile)
	if err != nil {
		return false
	}
	var tokens []int
	if err := json.Unmarshal(data, &tokens); err != nil {
		return false
	}
	for _, t := range tokens {
		if t == token {
			return true
		}
	}
	return false
}

func submitSongHandler(w http.ResponseWriter, r *http.Request) {
	// Enable CORS
	enableCORS(&w)

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var song Song
	if err := json.NewDecoder(r.Body).Decode(&song); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	if song.ItunesId == "" && song.Link == "" {
		http.Error(w, "Either link or itunesId is required", http.StatusBadRequest)
		return
	}

	if !checkToken(song.Token) {
		http.Error(w, "Token invalid", http.StatusUnauthorized)
		return
	}

	// Load existing submissions
	submissions := []Song{}
	if data, err := os.ReadFile(songSubmissionsFile); err == nil {
		_ = json.Unmarshal(data, &submissions)
	}

	// Remove previous submission with same token
	filtered := []Song{}
	for _, s := range submissions {
		if s.Token != song.Token {
			filtered = append(filtered, s)
		}
	}
	filtered = append(filtered, song)

	// Save updated submissions
	data, err := json.MarshalIndent(filtered, "", "  ")
	if err != nil {
		http.Error(w, "Failed to save submission", http.StatusInternalServerError)
		return
	}
	_ = os.WriteFile(songSubmissionsFile, data, 0644)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"detail": "success"}`))
}

func validateTokenHandler(w http.ResponseWriter, r *http.Request) {
	enableCORS(&w)
	w.Header().Set("Content-Type", "application/json")

	tokenStr := r.URL.Query().Get("token")
	token, err := strconv.Atoi(tokenStr)
	if err != nil {
		http.Error(w, `{"error":"Invalid token"}`, http.StatusBadRequest)
		return
	}

	if !checkToken(token) {
		http.Error(w, `{"error":"Token invalid"}`, http.StatusUnauthorized)
		return
	}

	// Look for existing submission by this token
	var submissions []Song
	var userSong *Song

	if data, err := os.ReadFile(songSubmissionsFile); err == nil {
		if err := json.Unmarshal(data, &submissions); err == nil {
			for _, s := range submissions {
				if s.Token == token {
					userSong = &s
					break
				}
			}
		}
	}

	response := map[string]interface{}{
		"valid": true,
	}

	if userSong != nil {
		response["data"] = userSong
	}

	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, `{"error":"Failed to encode response"}`, http.StatusInternalServerError)
	}
}

func enableCORS(w *http.ResponseWriter) {
	(*w).Header().Set("Access-Control-Allow-Origin", "*")
	(*w).Header().Set("Access-Control-Allow-Headers", "*")
	(*w).Header().Set("Access-Control-Allow-Methods", "*")
}

func main() {
	r := mux.NewRouter()

	r.HandleFunc("/send", submitSongHandler).Methods("POST", "OPTIONS")
	r.HandleFunc("/validate_token", validateTokenHandler).Methods("GET", "OPTIONS")

	// Basic CORS preflight handler
	r.Use(mux.CORSMethodMiddleware(r))

	log.Println("Server running on http://localhost:8000")
	log.Fatal(http.ListenAndServe(":8000", r))
}
