package main

import (
	"fmt"
	"image"
	"image/draw"
	"image/jpeg"
	"image/png"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"time"
)

const (
	ARQUIVO_BRUTO        = "ARQUIVO_BRUTO"
	RODAPE_LARGURA       = 526
	RODAPE_ALTURA        = 120
	POSICAO_HORIZONTAL   = 132
	POSICAO_VERTICAL     = 1224
	SALVAR_ARQUIVO_PRONTO = "ARTES_FINALIZADAS"
)

type File struct {
	DestFolder        string
	DestCompressFolder string
	Paths             []string
	Arts              []string
	Footers           []string
}

var PEGAR_ARQUIVO_BRUTO = []File{
	{
		DestFolder:        "ME_IGNORA/MG",
		DestCompressFolder: "MG",
		Paths:             []string{filepath.Join(ARQUIVO_BRUTO, "Artes", "MG"), filepath.Join(ARQUIVO_BRUTO, "Rodapes", "MG")},
	},
	// Add other entries here...
}

func main() {
	var files []File

	for _, item := range PEGAR_ARQUIVO_BRUTO {
		footers, _ := ioutil.ReadDir(item.Paths[1])
		arts, _ := ioutil.ReadDir(item.Paths[0])

		if len(footers) > 0 && len(arts) > 0 {
			files = append(files, File{
				DestFolder:         item.DestFolder,
				DestCompressFolder: item.DestCompressFolder,
				Paths:              item.Paths,
				Arts:               getNames(arts),
				Footers:            getNames(footers),
			})
		}
	}

	for _, file := range files {
		readFiles(file)
	}
}

func getNames(files []os.FileInfo) []string {
	var names []string
	for _, file := range files {
		names = append(names, file.Name())
	}
	return names
}

func readFiles(file File) {
	for _, footer := range file.Footers {
		for _, art := range file.Arts {
			if footer != ".DS_Store" && art != ".DS_Store" {
				watermark(footer, art, file.Paths, file.DestFolder, file.DestCompressFolder)
			}

			time.Sleep(150 * time.Millisecond)

			footerName := strings.Split(footer, ".")[0]
			fromPath := filepath.Join(SALVAR_ARQUIVO_PRONTO, file.DestFolder, footerName, art)
			toPath := filepath.Join(SALVAR_ARQUIVO_PRONTO, file.DestCompressFolder, footerName)

			compressImages(fromPath, toPath)
		}
	}
}

func watermark(footer, art string, paths []string, destFolder, destCompressFolder string) {
	footerName := strings.Split(footer, ".")[0]
	startTime := time.Now()

	footerImgFile, _ := os.Open(filepath.Join(paths[1], footer))
	defer footerImgFile.Close()
	footerImg, _ := jpeg.Decode(footerImgFile)

	imgFile, _ := os.Open(filepath.Join(paths[0], art))
	defer imgFile.Close()
	img, _ := jpeg.Decode(imgFile)

	offset := image.Pt(POSICAO_HORIZONTAL, POSICAO_VERTICAL)
	m := image.NewRGBA(img.Bounds())
	draw.Draw(m, img.Bounds(), img, image.Point{}, draw.Src)
	draw.Draw(m, footerImg.Bounds().Add(offset), footerImg, image.Point{}, draw.Over)

	out, _ := os.Create(filepath.Join(SALVAR_ARQUIVO_PRONTO, destFolder, footerName, art))
	defer out.Close()
	jpeg.Encode(out, m, nil)

	consoleResponse(footerName, destFolder, startTime)
}

func consoleResponse(footerName, destFolder string, startTime time.Time) {
	fmt.Printf("LICENCIADO: %s, modificou uma arte: %s, [INICIO]: %s [FIM]: %s\n", footerName, destFolder, toLocate(startTime), toLocate(time.Now()))
}

func toLocate(t time.Time) string {
	return t.Format("02/01/2006, 15:04:05")
}

func compressImages(fromPath, toPath string) {
	// Define the compression options for each file type
	options := map[string]map[string][]string{
		"jpg": {"engine": []string{"mozjpeg", "-quality", "60"}},
		"png": {"engine": []string{"pngquant", "--quality=20-50", "-o"}},
		"svg": {"engine": []string{"svgo", "--multipass"}},
		"gif": {"engine": []string{"gifsicle", "--colors", "64", "--use-col=web"}},
	}

	// Get the file extension (type)
	ext := strings.ToLower(filepath.Ext(fromPath))

	// Use the appropriate compression command for the file type
	if cmd, ok := options[ext]; ok {
		engine := cmd["engine"]

		// Compress the image using the command
		// This is a placeholder and may need to be replaced with actual compression code
		fmt.Printf("Compressing %s to %s using %s with options %v\n", fromPath, toPath, engine[0], engine[1:])

		// Simulate async compression with sleep
		time.Sleep(1 * time.Second)

		fmt.Printf("Compression of %s completed!\n", fromPath)
	} else {
		fmt.Printf("File type %s not supported.\n", ext)
	}
}
