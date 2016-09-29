package arxiv.browser

import akka.actor.{ActorSystem, Props}
import akka.http.scaladsl.server.Directives._
import akka.stream.ActorMaterializer
import akka.pattern.ask
import akka.util.Timeout

import scala.concurrent.duration._
import scala.concurrent.{Await, ExecutionContextExecutor}
import scala.language.postfixOps
import scala.util.{Failure, Success, Try}

trait Routes {
  implicit val system: ActorSystem
  implicit def executor: ExecutionContextExecutor
  implicit val materializer: ActorMaterializer
  implicit val timeout = Timeout(5.seconds)


  val routes = path("search") {
    get { search() }
  }

  def search() = {
    parameter("query") { query =>
      val dog = system.actorOf(Props[SearchUnit](new SearchUnit()))
      val response = ask(dog, SearchUnit.Query(query)).mapTo[SearchResponse.SearchResult]
      val result = Await.result(response, 1 day)
      complete { result.body.toString() }
    }
  }

}

