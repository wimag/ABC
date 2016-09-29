package arxiv.browser

import java.util._

import akka.actor.Actor
import akka.event.Logging

object SearchUnit {
  case class Query(text: String)
}

object SearchResponse {
  case class SearchResult(body: List[String])
}

class SearchUnit extends Actor {
  import SearchUnit._
  import SearchResponse._

  val log = Logging(context.system, this)

  override def receive: Receive = {
    case Query(text) => query(text)
  }

  def query(text: String) = {
    val response = new ArrayList[String]()
    response.add("test response")

    sender() ! new SearchResult(response)
  }
}
