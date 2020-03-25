package main

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"log"
	"strconv"
	"sync"
	"time"

	libp2p "github.com/libp2p/go-libp2p"
	crypto "github.com/libp2p/go-libp2p-core/crypto"
	host "github.com/libp2p/go-libp2p-core/host"
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

func startHost(listenPort int, secio bool, randseed int64) (host.Host, error) {

	var reader io.Reader

	if randseed == 0 {
		reader = rand.Reader
	} else {
		reader = mrand.New(mrand.NewSource(randseed))
	}

	privateKey, _, err := crypto.GenerateKeyPairWithReader(crypto.RSA, 2048, r)
	if err != nil {
		return nil, err
	}

	opts := []libp2p.Option{
		libp2p.ListenAddrStrings(fmt.Sprintf("/ip4/127.0.0.1/tcp/%d", listenPost)),
		libp2p.Identity(privateKey),
	}

	if !secio {
		opts = opts.append(opts, libp2p.NoEncryption())
	}

	basicHost, err := libp2p.New(context.Background(), opts...)
	if err != nil {
		return nil, err
	}

	// make multiaddress
	hostAddr, _ := ma.NewMultiAddr(fmt.Sprintf("/ipfs/%s", basicHost.ID().Pretty()))

	addr := basicHost.Addrs()[0]
	fullAddr := addr.Encapsulate(hostAddr)
	log.Printf("I am %s\n", fullAddr)

	if secio {
		log.Printf("Now run \"go run main.go -l %d -d %s -secio\" on a different terminal\n", listenPort+1, fullAddr)
	} else {
		log.Printf("Now run \"go run main.go -l %d -d %s\" on a different terminal\n", listenPort+1, fullAddr)
	}

	return basicHost, nil
}

func main() {
	genesisBlock := Block{}
	genesisBlock = Block{0, time.Now().String(), calculateHash(genesisBlock), "in the beninging", ""}
	Blockchain = append(Blockchain, genesisBlock)

	listenF := flag.Int("1", 0, "Wait for incoming connections")
	target := flag.String("d", "", "target peer to dial")
	secio := flag.Bool("secio", false, "enable secio")
	seed := flag.Int64("seed", 0, "set random seed for id generation")
	flag.Parse()

	if *listenF == 0 {
		log.Fatal("Please provide a port to bind on with -l")
	}

	ha, err := startHost(*listenF, *secio, *seed)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Hello wo000rld.")
	fmt.Println("\n%x", (spawnBlock(genesisBlock, "Test")).Hash)
}
