class Sdl2Gfx < Formula
  desc "SDL2 graphics drawing primitives and other support functions"
  homepage "https://www.ferzkopp.net/wordpress/2016/01/02/sdl_gfx-sdl2_gfx/"
  url "https://www.ferzkopp.net/Software/SDL2_gfx/SDL2_gfx-1.0.4.tar.gz"
  mirror "https://sources.voidlinux.org/SDL2_gfx-1.0.4/SDL2_gfx-1.0.4.tar.gz"
  sha256 "63e0e01addedc9df2f85b93a248f06e8a04affa014a835c2ea34bfe34e576262"
  license "Zlib"

  livecheck do
    url :homepage
    regex(/href=.*?SDL2_gfx[._-]v?(\d+(?:\.\d+)+)\.t/i)
  end

  depends_on "sdl2"

  def install
    extra_args = []
    extra_args << "--disable-mmx" if Hardware::CPU.arm?

    system "./configure", "--disable-dependency-tracking",
                          "--prefix=#{prefix}",
                          "--disable-sdltest",
                          *extra_args
    system "make", "install"
  end

  test do
    (testpath/"test.c").write <<~EOS
      #include <SDL2/SDL2_imageFilter.h>

      int main()
      {
        int mmx = SDL_imageFilterMMXdetect();
        return 0;
      }
    EOS
    system ENV.cc, "test.c", "-L#{lib}", "-lSDL2_gfx", "-o", "test"
    system "./test"
  end
end
