//
//  ViewController.swift
//  Trip-Planner
//
//  Created by Sunny Ouyang on 10/14/17.
//  Copyright © 2017 Sunny Ouyang. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var emailTextField: UITextField!
    
    @IBOutlet weak var passwordTextField: UITextField!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

   
    @IBAction func signUpTapped(_ sender: Any) {
    }
    
    //When the login button is tapped, we want to send a GET request. First we have to turn the email and password into a token, ans pass them off in the authorization header of the request. 
    
    @IBAction func loginTapped(_ sender: Any) {
    }
    
    
    

}

