//
//  user.swift
//  Trip-Planner
//
//  Created by Sunny Ouyang on 10/15/17.
//  Copyright © 2017 Sunny Ouyang. All rights reserved.
//

import Foundation
import UIKit


//this is the model we're trying to convert our data to
struct User {
    var username: String
//    var password: String
    var email: String
    
}

//this is allowing the data to be decoded back to our User model 

extension User: Decodable {
    
    enum userKeys: String, CodingKey {
        case username
//        case password
        case email
    }
    
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: userKeys.self)
        let username = try container.decode(String.self, forKey: .username)
//        let password = try container.decode(String.self, forKey: .password)
        let email = try container.decode(String.self, forKey: .email)
        
        self.init(username: username, email: email)
    }
    
}
