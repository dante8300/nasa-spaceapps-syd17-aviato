import { Injectable } from '@angular/core';
//import { Platform } from 'ionic-angular';
 
declare var Connection;
 
@Injectable()
export class Connectivity {
 
  isOnline(): boolean {
      return navigator.onLine; 
  }
 
  isOffline(): boolean {
      return !navigator.onLine;   
  }
}