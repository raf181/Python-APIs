package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"

	"github.com/gorilla/mux"
)

// Credentials struct to represent username, password, program name, and API key
type Credentials struct {
	Username string `json:"username"`
	Password string `json:"password"`
	Program  string `json:"program"`
	APIKey   string `json:"api_key"`
}

// Function to load user credentials from the users.json file
func loadUsers() ([]Credentials, error) {
	file, err := os.ReadFile("users.json")
	if err != nil {
		return nil, err
	}

	var users []Credentials
	err = json.Unmarshal(file, &users)
	if err != nil {
		return nil, err
	}

	return users, nil
}

// Function to validate credentials
func isValidCredentials(creds Credentials, users []Credentials) bool {
	for _, user := range users {
		if creds.Username == user.Username && creds.Password == user.Password && creds.APIKey == user.APIKey {
			return true
		}
	}
	return false
}

// Function to handle API requests
func handleRequest(w http.ResponseWriter, r *http.Request) {
	users, err := loadUsers()
	if err != nil {
		http.Error(w, "Error loading user data", http.StatusInternalServerError)
		return
	}

	var creds Credentials
	err = json.NewDecoder(r.Body).Decode(&creds)
	if err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	// Validate credentials (implement your own validation logic)
	if !isValidCredentials(creds, users) {
		http.Error(w, "Invalid credentials", http.StatusUnauthorized)
		return
	}

	// Construct the path to the user's program JSON file
	programPath := filepath.Join("Programs", creds.Username, creds.Program+".json")

	// Read the program JSON file
	programData, err := ioutil.ReadFile(programPath)
	if err != nil {
		http.Error(w, "Error reading program data", http.StatusInternalServerError)
		return
	}

	// Respond with the program variables
	w.Header().Set("Content-Type", "application/json")
	w.Write(programData)
}

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/api", handleRequest).Methods("POST")

	// Start the server
	fmt.Println("Server listening on port 8080...")
	http.ListenAndServe(":8080", r)
}
