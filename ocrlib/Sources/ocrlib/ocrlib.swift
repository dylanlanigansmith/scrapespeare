// The Swift Programming Language
// https://docs.swift.org/swift-book
import Foundation
import Vision
import CoreImage

//@objc public class TextExtractor: NSObject {
   @_cdecl("extractText") public func extractText(fromImageData imageData: UnsafeRawPointer, length: Int) -> UnsafeMutablePointer<CChar>? {
        let data = Data(bytes: imageData, count: length)
        guard let image = CIImage(data: data) else {
            return strdup("Unable to create image from data")
        }
  
    var results: [[String: Any]] = []
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

                 results.append([
                                "text": String(character),
                                "boundingBox": ["x": rect.origin.x, "y": rect.origin.y, "width": rect.size.width, "height": rect.size.height]
                            ])
              }
              lineWords[lineWords.count - 1] += String(character)
            }
          }
          
        
        //texts.append(lineWords)
        //positions.append(lineRects)
        }
      }
    }
    
    textRequest.recognitionLevel = .accurate

    do {
        try requestHandler.perform([textRequest])
    } catch {
        print("Failed to perform text request: \(error)")
    }

        let result: [String: Any] = ["texts": texts, "positions": positions.map { $0.map { ["x": $0.origin.x, "y": $0.origin.y, "width": $0.size.width, "height": $0.size.height] } }]
        
        if let jsonData = try? JSONSerialization.data(withJSONObject: results, options: []),
            let jsonString = String(data: jsonData, encoding: .utf8) {
            return strdup(jsonString)
        } else {
            return strdup("{\"error\": \"Failed to serialize result to JSON\"}")
        }
        // texts and positions need to be returned somehow we can access in python
        
    }
//}
