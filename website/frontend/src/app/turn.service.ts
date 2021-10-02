import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class TurnService {

  constructor(private http: HttpClient) { }

  private turnEndpoint = '/';

  takeATurn(state: object){
    return this.http.post(this.turnEndpoint, {state});
  }
}



