import Foundation
import Vision
import CoreImage
func extractText(from imageURL: URL) {
    let ciImage = CIImage(contentsOf: imageURL)
    guard let image = ciImage else {
        print("Unable to load image")
        return
    }

    let requestHandler = VNImageRequestHandler(ciImage: image, options: [:])
    let textRequest = VNRecognizeTextRequest { (request, error) in
        if let error = error {
            print("Error recognizing text: \(error)")
            return
        }

        guard let observations = request.results as? [VNRecognizedTextObservation] else {
            print("No text found")
            return
        }

        for observation in observations {
            if let topCandidate = observation.topCandidates(1).first {
                let recognizedText = topCandidate.string
                let boundingBox = observation.boundingBox

                print("Text: '\(recognizedText)'")
                print("Bounding Box: \(boundingBox)")
                print("----------------------------")
            }
        }
         for observation in observations {
        guard let topCandidate = observation.topCandidates(1).first else { continue }
        
        
        var lineWords: [String] = []
        var lineRects: [CGRect] = []
        
        var lineBoundingBoxs: [CGRect] = []
        
        for (index, character) in topCandidate.string.enumerated() {
          let startIndex = topCandidate.string.index(topCandidate.string.startIndex, offsetBy: index)
          let endIndex = topCandidate.string.index(startIndex, offsetBy: 1)
          
          let range = startIndex..<endIndex
          
          if let wordBox = try? topCandidate.boundingBox(for: range) {
            let boundingBox = wordBox.boundingBox
            if character != " " {
              if boundingBox != lineBoundingBoxs.last {
                lineWords.append("")
                lineBoundingBoxs.append(boundingBox)
                let rect = CGRect(x: boundingBox.minX, y: 1 - boundingBox.maxY - boundingBox.height, width: boundingBox.width, height: boundingBox.height)
                lineRects.append(rect)
              }
              lineWords[lineWords.count - 1] += String(character)
            }
          }
          
          print(lineWords)
          print(lineRects)
        }
      }
    }
    
    textRequest.recognitionLevel = .accurate

    do {
        try requestHandler.perform([textRequest])
    } catch {
        print("Failed to perform text request: \(error)")
    }
}

func main() {
    guard CommandLine.arguments.count > 1 else {
        print("Usage: TextExtractor <image-path>")
        return
    }

    let imagePath = CommandLine.arguments[1]
    let imageURL = URL(fileURLWithPath: imagePath)
    print(imagePath)
    extractText(from: imageURL)
}

main()
