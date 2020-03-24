package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"strconv"
	"sync"
	"time"
)

// Block Constructor struct
type Block struct {
	Index     int
	Timestamp string
	Hash      string
	Data      string
	PrevHash  string
}

// Blockchain variable
var Blockchain []Block

var mutex = &sync.Mutex{}

// Checks if there is any error in the block's Index, and hashes
// If none return True as in "Passed Integrity Checks"
func validateBlockIntegrity(currentBlock, prevBlock Block) bool {
	if prevBlock.Index+1 != currentBlock.Index {
		return false
	}
	if prevBlock.Hash != currentBlock.PrevHash {
		return false
	}
	if calculateHash(currentBlock) != currentBlock.Hash {
		return false
	}

	return true
}

// Calculates the Hash of the new block by concatenating Index,
// timestamp, data and previous hash as string data
func calculateHash(block Block) string {
	bdt := strconv.Itoa(block.Index) + block.Timestamp + block.Data + block.PrevHash
	// Use sha256 to hash.
	// Current iteration is very rudimentary.
	// Can layer with other stuff to harden it
	tempHash := sha256.New()
	tempHash.Write([]byte(bdt))
	hashed := tempHash.Sum(nil)
	// encodes back to string
	return hex.EncodeToString(hashed)
}

// Takes in previous block and string data of new block.
// Returns a new Block.
func spawnBlock(prevBlock Block, Data string) Block {
	var block Block

	// Gets current time to act as Timestamp
	t := time.Now()

	block.Index = prevBlock.Index + 1
	block.Timestamp = t.String()
	block.Data = Data
	block.PrevHash = prevBlock.Hash
	block.Hash = calculateHash(block)

	return block
}

func main() {
	fmt.Println("Hello wo000rld.")
}
