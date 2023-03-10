package cz.kiv.vi.datavisualization.controllers;


import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/v2/beta")
public class MainController {


    @GetMapping(value = "/hello", produces = "application/json")
    public ResponseEntity<String> helloWorld() {

        String output = "{\"message\": \"hello world\"}";
        return ResponseEntity.ok().body(output);
    }

}
