package main

import (
    "fmt"
    "github.com/buger/jsonparser"
    "io"
    "io/ioutil"
    "log"
    "net/http"
    "os"
)

var productDB []map[string]interface{}

func processPayment(w http.ResponseWriter, r *http.Request) {
    var total int64 = 0
    var getFlag bool = false
    var result string = "{}"
    data, _ := ioutil.ReadAll(r.Body)
    jsonparser.ArrayEach(
        data,
        func(value []byte, dataType jsonparser.ValueType, offset int, err error) {
            id, _ := jsonparser.GetInt(value, "id")
            qty, _ := jsonparser.GetInt(value, "qty")
            total = total + productDB[id]["price"].(int64) * qty
            if id == 10 {
                getFlag = true
            }
        },
        "cart")

    if total > 1000 {
        result = fmt.Sprintf("{\"error\": \"Not enough money. You only have 1000.\"}")
    } else if getFlag {
        result = fmt.Sprintf("{\"flag\": \"%s\"}", os.Getenv("FLAG"))
    } else {
        result = fmt.Sprintf("{\"total\": %d}", total)
    }
    io.WriteString(w, result)
}

func main() {
    // Initialize ProductDB
    data, err := ioutil.ReadFile("/app/productDB.json")
    if err != nil {
        panic(err)
    }
    // Database init
    jsonparser.ArrayEach(data, func(value []byte, dataType jsonparser.ValueType, offset int, err error) {
        m := make(map[string]interface{})
        m["name"], _ = jsonparser.GetString(value, "name")
        m["price"], _ = jsonparser.GetInt(value, "price")
        productDB = append(productDB, m)
    })

    // Start Web server
    mux := http.NewServeMux()
    mux.HandleFunc("/process", processPayment)

    err = http.ListenAndServe(":8000", mux)
    log.Fatal(err)
}
