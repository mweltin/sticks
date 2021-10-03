import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class TurnService {

  constructor(private http: HttpClient) { }

  private turnEndpoint = '/turn';

  takeATurn(turnData: object){
    return this.http.post(this.turnEndpoint, {turnData});
  }
}



