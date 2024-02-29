package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
)

// Counter holds the visit count and a mutex to synchronize access to it.
type Counter struct {
	count int
	mux   sync.Mutex
}

// ServeHTTP serves the HTTP request and increments the visit count if the request is for the HTML content.
func (c *Counter) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Check if the request is for the HTML content.
	if r.URL.Path == "/" && strings.HasPrefix(r.Header.Get("Accept"), "text/html") {
		// Lock the mutex to ensure atomic access to the count.
		c.mux.Lock()
		defer c.mux.Unlock()

		// Increment the visit count.
		c.count++
	}

	// Write the response with the visit count.
	fmt.Fprintf(w, `
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Bootstrap CSS -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">

        <title>Counter</title>
      </head>
      <body>
        <div class="container d-flex align-items-center justify-content-center" style="height: 100vh;">
          <h1 class="display-1">Welcome to the website! You are visitor number <b>%d</b>.</h1>
        </div>

        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
      </body>
    </html>
    `, c.count)
}

func main() {
	// Create a new Counter.
	counter := &Counter{}

	// Register the Counter as the handler for the root path ("/").
	http.Handle("/", counter)

	port := os.Getenv("PORT")
	if port == "" {
		port = "5000"
	}
	http.ListenAndServe(":"+port, nil)
}
